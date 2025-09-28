from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from helpers.helpers import create_id
from models.models import Player
from config.db import SessionLocal
from flask_jwt_extended import create_access_token
import datetime

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

        hashed_password = bcrypt.generate_password_hash(password)

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
        access_token = create_access_token(identity=player.id, expires_delta=expires)
        session.commit()
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400

    finally:
        session.close()
