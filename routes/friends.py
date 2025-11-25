from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import delete, insert
from models.models import Player, t_friend
from config.db import SessionLocal

friends = Blueprint("friends", __name__)

# CHECAR SOLICITUDES


@friends.route("/friends/check_requests", methods=["GET"])
@jwt_required()
def get_requests():
    try:
        player_id = get_jwt_identity()
        session = SessionLocal()

        requests = (
            session.query(t_friend, Player.username)
            .join(Player, Player.id == t_friend.c.petitioner)
            .filter(
                (
                    (t_friend.c.id1 == player_id) | (t_friend.c.id2 == player_id)
                ),  # el user es parte
                t_friend.c.petitioner != player_id,  # no fue él quien envió
                t_friend.c.approved == 0,  # aún no aceptadas
            )
            .all()
        )
        if not requests:
            return jsonify({"message": "No friend requests found"}), 404

        requests_json = []
        for req in requests:
            requests_json.append(
                {
                    "id1": req.id_min,
                    "id2": req.id_max,
                    "petitioner_name": req.username,
                    "petitoner": req.petitioner,
                    "approved": req.approved,
                }
            )
        return jsonify(requests_json), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Mandar SOLICITUDES
@friends.route("/friends/send_request", methods=["POST"])
@jwt_required()
def send_request():
    try:
        data = request.get_json()

        sender_id = get_jwt_identity()
        receiver_id = data.get("receiver_id")

        if not receiver_id:
            raise ValueError("No receiver player id")

        session = SessionLocal()

        receiver_player_data = (
            session.query(Player).filter(Player.id == receiver_id).first()
        )

        if not receiver_player_data:
            raise ValueError("That Player does not exist")

        query = insert(t_friend).values(
            id1=sender_id, id2=receiver_id, petitioner=sender_id
        )

        session.execute(query)
        session.commit()

        return jsonify({"message": f"Sent friend request to {receiver_id}"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# ACEPTAR SOLICITUDES
@friends.route("/friends/accept_request", methods=["POST"])
@jwt_required()
def accept_request():
    try:
        data = request.get_json()
        friend_id = data.get("friend_id")
        player_id = get_jwt_identity()

        if not friend_id:
            return jsonify({"message": "friend_id is required"}), 400

        session = SessionLocal()

        # Buscar la relación en cualquier orden
        request_entry = (
            session.query(t_friend)
            .filter(
                ((t_friend.c.id1 == player_id) & (t_friend.c.id2 == friend_id))
                | ((t_friend.c.id1 == friend_id) & (t_friend.c.id2 == player_id)),
                t_friend.c.approved == 0,
            )
            .first()
        )

        if not request_entry:
            return jsonify({"message": "No pending request found"}), 404

        # Actualizar approved -> 1
        session.execute(
            t_friend.update()
            .where(
                ((t_friend.c.id1 == player_id) & (t_friend.c.id2 == friend_id))
                | ((t_friend.c.id1 == friend_id) & (t_friend.c.id2 == player_id))
            )
            .values(approved=1)
        )
        session.commit()

        friend_player = session.query(Player).filter(Player.id == friend_id).first()
        friend_name = friend_player.username

        return jsonify({"message": f"Friend request with {friend_name} accepted"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# RECHAZAR SOLICITUDES
@friends.route("/friends/deny_request", methods=["DELETE"])
@jwt_required()
def deny_requests():
    try:
        data = request.get_json()
        friend_id = data.get("friend_id")
        player_id = get_jwt_identity()

        if not friend_id:
            return jsonify({"message": "friend_id is required"}), 400

        session = SessionLocal()

        # Eliminar la solicitud
        session.execute(
            delete(t_friend).where(
                ((t_friend.c.id1 == player_id) & (t_friend.c.id2 == friend_id))
                | ((t_friend.c.id1 == friend_id) & (t_friend.c.id2 == player_id))
                & t_friend.c.approved
                == 0
            )
        )
        session.commit()

        return jsonify({"message": f"Friend request denied"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Ver amigos
@friends.route("/friends/list", methods=["GET"])
@jwt_required()
def list_friends():
    try:
        player_id = get_jwt_identity()
        session = SessionLocal()

        # Buscar todas las relaciones donde el jugador esté en id1 o id2 y approved=1
        friend_entries = (
            session.query(t_friend)
            .filter(
                ((t_friend.c.id1 == player_id) | (t_friend.c.id2 == player_id)),
                t_friend.c.approved == 1,
            )
            .all()
        )

        if not friend_entries:
            return jsonify({"friends": []}), 200

        friends = []
        for entry in friend_entries:
            # El amigo es el que NO es player_id
            friend_id = entry.id2 if entry.id1 == player_id else entry.id1
            friend_player = session.query(Player).filter(Player.id == friend_id).first()

            if friend_player:
                friends.append(
                    {
                        "id": friend_player.id,
                        "username": friend_player.username,
                    }
                )

        return jsonify({"friends": friends}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


# Borrar amigo
@friends.route("/friends/remove", methods=["DELETE"])
@jwt_required()
def remove_friend():
    try:
        data = request.get_json()
        friend_id = data.get("friend_id")
        player_id = get_jwt_identity()

        if not friend_id:
            return jsonify({"message": "friend_id is required"}), 400

        session = SessionLocal()

        result = session.execute(
            t_friend.delete().where(
                ((t_friend.c.id1 == player_id) & (t_friend.c.id2 == friend_id))
                | ((t_friend.c.id1 == friend_id) & (t_friend.c.id2 == player_id)),
                t_friend.c.approved == 1,
            )
        )

        session.commit()

        if result.rowcount == 0:
            return jsonify({"message": "Friendship not found"}), 404

        return jsonify({"message": f"Friendship with {friend_id} removed"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()
