from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from config.db import SessionLocal
from models.models import Trade, TradeStatus, Player, PokemonOwned, PokemonStat
import uuid
from datetime import datetime

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
            return (
                jsonify({"message": "One of the Pokémon in this trade does not exist"}),
                404,
            )

        requester_pokemon.player_id, receiver_pokemon.player_id = (
            receiver_pokemon.player_id,
            requester_pokemon.player_id,
        )

        session.commit()

        return (
            jsonify(
                {
                    "message": f"Trade with id: {trade_id} has been confirmed successfully"
                }
            ),
            202,
        )
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
    try:
        trades = (
            session.query(
                Trade,
                Player.username.label("requester_name"),
                PokemonOwned.label("requester_pokemon"),
                PokemonStat.label("requester_stats"),
                PokemonOwned,  # receiver pokemon
                PokemonStat,  # receiver stats
            )
            .join(Player, Player.id == Trade.requester_id)
            .join(PokemonOwned, PokemonOwned.id == Trade.requester_pokemon_id)
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .join(PokemonOwned, PokemonOwned.id == Trade.receiver_pokemon_id)
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .filter(Trade.receiver_id == player_id, Trade.status == TradeStatus.pending)
            .all()
        )

        result = []
        for (
            t,
            requester_name,
            requester_pokemon,
            requester_stats,
            receiver_pokemon,
            receiver_stats,
        ) in trades:
            result.append(
                {
                    "trade_id": t.id,
                    "from_user": requester_name,
                    # Pokémon que ofrece
                    "requester_pokemon_id": requester_pokemon.id,
                    "requester_pokemon_name": requester_stats.name,
                    "requester_pokedex": requester_pokemon.pokedex_number,
                    # Pokémon que quiere obtener
                    "receiver_pokemon_id": receiver_pokemon.id,
                    "receiver_pokemon_name": receiver_stats.name,
                    "receiver_pokedex": receiver_pokemon.pokedex_number,
                }
            )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()
