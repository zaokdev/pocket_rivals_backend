from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from helpers.helpers import create_id
from models.models import Player
from config.db import SessionLocal
from flask_jwt_extended import create_access_token
import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required

player = Blueprint("player", __name__)

bcrypt = Bcrypt()


# Registrar nuevo usuario
@player.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    id = create_id(32)
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing information"}), 400

    email = email.strip().lower()

    try:
        session = SessionLocal()
        existingPlayer = (
            session.query(Player)
            .filter(or_(Player.email == email, Player.username == username))
            .first()
        )

        if existingPlayer:
            raise FileExistsError("Player already registered")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        newPlayer = Player(
            id=id, username=username, email=email, password=hashed_password
        )

        session.add(newPlayer)
        session.commit()
        return jsonify({"message": "Player Created"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        session.close()


# Login de usuario
@player.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Log In information missing"}), 400

    email = email.strip().lower()

    try:
        session = SessionLocal()
        player = session.query(Player).filter(Player.email == email).first()
        if not player:
            raise FileNotFoundError("Player not found")

        correctPassword = bcrypt.check_password_hash(
            pw_hash=player.password, password=password
        )

        if not correctPassword:
            raise ValueError("Incorrect Password Given")

        expires = datetime.timedelta(hours=2)
        access_token = create_access_token(
            identity=player.id,
            expires_delta=expires,
            additional_claims={
                "user": player.username,
                "profile_picture": player.profile_picture,
            },
        )
        session.commit()
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        session.close()


@player.route("/player/change_username", methods=["PUT"])
@jwt_required()
def change_username():
    session = SessionLocal()
    try:
        data = request.get_json()

        new_username = data.get("username")
        player_id = get_jwt_identity()

        if not new_username:
            return jsonify({"message": "Username missing"}), 400

        existing_player = (
            session.query(Player).filter(Player.username == new_username).first()
        )

        if existing_player:
            return jsonify({"message": "Username already taken"}), 400

        player = session.query(Player).filter(Player.id == player_id).first()

        if not player:
            return jsonify({"message": "Player not found"}), 404

        player.username = new_username
        session.commit()

        return jsonify({"message": "Username updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


@player.route("/player/change_profile_picture", methods=["PUT"])
@jwt_required()
def change_profile_picture():
    session = SessionLocal()
    try:
        data = request.get_json()
        new_picture = data.get("profile_picture")
        player_id = get_jwt_identity()

        if not new_picture:
            return jsonify({"message": "Missing profile_picture"}), 400

        player = session.query(Player).filter(Player.id == player_id).first()

        if not player:
            return jsonify({"message": "Player not found"}), 404

        player.profile_picture = new_picture
        session.commit()

        return jsonify({"message": "Profile picture updated successfully"}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


@player.route("/player/<id>", methods=["GET"])
@jwt_required()
def get_player(id):
    try:
        session = SessionLocal()
        player = session.query(Player).filter(Player.id == id).first()

        if not player:
            return jsonify({"message": "Player not found"}), 404

        return (
            jsonify(
                {
                    "id": player.id,
                    "username": player.username,
                    "profile_picture": player.profile_picture,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()
