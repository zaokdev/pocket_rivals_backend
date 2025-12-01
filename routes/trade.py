from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from config.db import SessionLocal
from models.models import Trade, TradeStatus, Player, PokemonOwned, PokemonStat
import uuid
from datetime import datetime
from sqlalchemy.orm import aliased
from events import connected_users
from extensions import socketio

trade = Blueprint("trade", __name__)


@trade.route("/trade/<string:friend_id>", methods=["GET"])
@jwt_required()
def get_requests_specific(friend_id):
    trainer_id = get_jwt_identity()
    session = SessionLocal()
    try:
        trades = (
            session.query(Trade)
            .filter(
                ((Trade.requester_id == trainer_id) & (Trade.receiver_id == friend_id))
                | (
                    (Trade.requester_id == friend_id)
                    & (Trade.receiver_id == trainer_id)
                ),
                Trade.status == TradeStatus.pending,
            )
            .all()
        )
        if not trades:
            return jsonify({"message": "No pending trades with that friend"}), 404

        trades_json = []
        for t in trades:
            trades_json.append(
                {
                    "id": t.id,
                    "requester_id": t.requester_id,
                    "receiver_id": t.receiver_id,
                    "requester_pokemon_id": t.requester_pokemon_id,
                    "receiver_pokemon_id": t.receiver_pokemon_id,
                    "status": t.status.value,
                    "created_at": t.created_at,
                    "decided_at": t.decided_at,
                }
            )

        return jsonify(trades_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()


# Mandar un petición de intercambio
@trade.route("/trade/send", methods=["POST"])
@jwt_required()
def request_pokemon():
    player_id = get_jwt_identity()
    data = request.get_json()
    friend_id = data.get("friend_id")
    requester_pokemon_id = data.get("requester_pokemon_id")
    receiver_pokemon_id = data.get("receiver_pokemon_id")

    if not friend_id or not requester_pokemon_id or not receiver_pokemon_id:
        return jsonify({"message": "Parameters missing"}), 400

    session = SessionLocal()
    try:
        # Verificar si el Pokémon del requester ya está en un trade pendiente
        existing_trade_requester = (
            session.query(Trade)
            .filter(
                (
                    (Trade.requester_pokemon_id == requester_pokemon_id)
                    | (Trade.receiver_pokemon_id == requester_pokemon_id)
                ),
                Trade.status == TradeStatus.pending,
            )
            .first()
        )

        if existing_trade_requester:
            return (
                jsonify(
                    {"message": "Este Pokémon ya está en un intercambio pendiente."}
                ),
                400,
            )

        # Verificar si el Pokémon del receiver ya está en un trade pendiente
        existing_trade_receiver = (
            session.query(Trade)
            .filter(
                (
                    (Trade.requester_pokemon_id == receiver_pokemon_id)
                    | (Trade.receiver_pokemon_id == receiver_pokemon_id)
                ),
                Trade.status == TradeStatus.pending,
            )
            .first()
        )

        if existing_trade_receiver:
            return (
                jsonify(
                    {
                        "message": "El Pokémon seleccionado ya está en un intercambio pendiente."
                    }
                ),
                400,
            )

        trade = Trade(
            id=str(uuid.uuid4()),
            requester_id=player_id,
            receiver_id=friend_id,
            requester_pokemon_id=requester_pokemon_id,
            receiver_pokemon_id=receiver_pokemon_id,
            status=TradeStatus.pending,
            created_at=datetime.now(),
        )

        session.add(trade)
        session.commit()
        return jsonify({"message": "Trade Request created"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Confirmando el intercambio de pokemon
@trade.route("/trade/confirm", methods=["POST"])
@jwt_required()
def confirm_request():

    player_id = get_jwt_identity()
    data = request.get_json()
    trade_id = data.get("trade_id")

    if not trade_id:
        return jsonify({"message": "Trade_id is necessary"}), 400

    session = SessionLocal()

    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()

        if not trade:
            return jsonify({"message": "Trade not found"}), 404

        if trade.receiver_id != player_id:
            return jsonify({"message": "You cannot confirm this trade"}), 403

        if trade.status != TradeStatus.pending:
            return jsonify({"message": "Trade already decided"}), 400

        requester_user = (
            session.query(Player).filter(Player.id == trade.requester_id).first()
        )
        receiver_user = (
            session.query(Player).filter(Player.id == trade.receiver_id).first()
        )

        trade.status = TradeStatus.accepted
        trade.decided_at = datetime.now()

        requester_pokemon = (
            session.query(PokemonOwned)
            .filter(PokemonOwned.id == trade.requester_pokemon_id)
            .first()
        )
        receiver_pokemon = (
            session.query(PokemonOwned)
            .filter(PokemonOwned.id == trade.receiver_pokemon_id)
            .first()
        )

        if not requester_pokemon or not receiver_pokemon:
            return jsonify({"message": "Pokémon missing"}), 404

        requester_pokemon.player_id, receiver_pokemon.player_id = (
            receiver_pokemon.player_id,
            requester_pokemon.player_id,
        )

        session.commit()

        requester_id = trade.requester_id

        if requester_id in connected_users:
            print("Enviando notificación al usuario creador:", requester_id)

            socketio.emit(
                "trade_accepted",
                {
                    "trade_id": trade_id,
                    "message": "Tu intercambio fue aceptado",
                    "other_username": receiver_user.username,
                },
                room=connected_users[requester_id],
            )
        else:
            print("Usuario no conectado, no se puede enviar WS")

        return jsonify({"message": "Trade confirmed successfully"}), 202

    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Denegando el intercambio de Pokemon
@trade.route("/trade/deny", methods=["POST"])
@jwt_required()
def deny_request():
    player_id = get_jwt_identity()
    data = request.get_json()
    trade_id = data.get("trade_id")

    if not trade_id:
        return jsonify({"message": "Trade_id is neccesary for this method"}), 400

    session = SessionLocal()

    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()

        if not trade:
            return jsonify({"message": "That pending trade doesn't exist"}), 404

        if trade.receiver_id != player_id:
            return (
                jsonify({"message": "You are not authorized to confirm this trade"}),
                403,
            )

        if trade.status != TradeStatus.pending:
            return jsonify({"message": "Trade already decided"}), 400

        trade.status = TradeStatus.rejected
        trade.decided_at = datetime.now()

        session.commit()

        return (
            jsonify({"message": f"Trade with id: {trade_id} has been denied"}),
            200,
        )
    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()


# Obtener todas las solicitudes de intercambio pendientes
@trade.route("/trade/pending_requests", methods=["GET"])
@jwt_required()
def get_pending_trades():
    player_id = get_jwt_identity()
    session = SessionLocal()

    # Aliases for clean joins
    RequesterOwned = aliased(PokemonOwned)
    ReceiverOwned = aliased(PokemonOwned)
    RequesterStat = aliased(PokemonStat)
    ReceiverStat = aliased(PokemonStat)

    try:
        trades = (
            session.query(
                Trade.id.label("trade_id"),
                # requester info
                Player.username.label("requester_name"),
                RequesterStat.name.label("requester_pokemon_name"),
                RequesterStat.pokedex_number.label("requester_pokedex"),
                RequesterOwned.id.label("requester_pokemon_id"),
                # receiver info (your Pokémon)
                ReceiverOwned.id.label("receiver_pokemon_id"),
                ReceiverStat.name.label("receiver_pokemon_name"),
                ReceiverStat.pokedex_number.label("receiver_pokedex"),
            )
            # JOINS for requester
            .join(Player, Player.id == Trade.requester_id)
            .join(RequesterOwned, RequesterOwned.id == Trade.requester_pokemon_id)
            .join(
                RequesterStat,
                RequesterStat.pokedex_number == RequesterOwned.pokedex_number,
            )
            # JOINS for receiver (you)
            .join(ReceiverOwned, ReceiverOwned.id == Trade.receiver_pokemon_id)
            .join(
                ReceiverStat,
                ReceiverStat.pokedex_number == ReceiverOwned.pokedex_number,
            )
            # Only trades pending for this player
            .filter(Trade.receiver_id == player_id)
            .filter(Trade.status == TradeStatus.pending)
            .all()
        )

        result = []
        for row in trades:
            result.append(
                {
                    "trade_id": row.trade_id,
                    "from_user": row.requester_name,
                    # offered Pokémon (their Pokémon)
                    "pokemon_offered": row.requester_pokemon_name,
                    "pokemon_offered_number": row.requester_pokedex,
                    "requester_pokemon_id": row.requester_pokemon_id,
                    # your Pokémon
                    "your_pokemon_name": row.receiver_pokemon_name,
                    "your_pokemon_number": row.receiver_pokedex,
                    "your_pokemon_id": row.receiver_pokemon_id,
                }
            )

        return jsonify(result), 200

    except Exception as e:
        print("ERROR EN TRADE REQUESTS:", e)
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Obtener todas mis solicitudes de intercambio pendientes
@trade.route("/trade/my_requests", methods=["GET"])
@jwt_required()
def get_my_outgoing_requests():
    player_id = get_jwt_identity()
    session = SessionLocal()
    try:
        trades = (
            session.query(Trade)
            .filter(Trade.requester_id == player_id)
            .filter(Trade.status == TradeStatus.pending)
            .all()
        )

        result = []
        for t in trades:
            result.append(
                {
                    "trade_id": t.id,
                    "requester_pokemon_id": t.requester_pokemon_id,
                    "receiver_pokemon_id": t.receiver_pokemon_id,
                    "status": t.status.value,
                }
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()


# Obtener los Pokémon bloqueados de un amigo
@trade.route("/trade/blocked_pokemon/<string:friend_id>", methods=["GET"])
@jwt_required()
def get_blocked_pokemon(friend_id):
    player_id = get_jwt_identity()
    session = SessionLocal()

    try:
        trades = (
            session.query(Trade)
            .filter(
                (
                    (Trade.requester_id == friend_id)
                    & (Trade.status == TradeStatus.pending)
                )
                | (
                    (Trade.receiver_id == friend_id)
                    & (Trade.status == TradeStatus.pending)
                )
            )
            .all()
        )

        blocked_pokemon_ids = []
        for trade in trades:
            blocked_pokemon_ids.append(trade.requester_pokemon_id)
            blocked_pokemon_ids.append(trade.receiver_pokemon_id)

        print(
            f"Bloqueados de {friend_id}: {blocked_pokemon_ids}"
        )  # Verifica si los Pokémon están correctos.

        return jsonify({"blocked_pokemon_ids": blocked_pokemon_ids}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()
