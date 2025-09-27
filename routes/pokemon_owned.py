from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from config.db import SessionLocal
from models.models import PokemonOwned, PokemonStat


pokemon_owned = Blueprint("pokemon_owned", __name__)


@pokemon_owned.route("/pokemon/get_all_owned", methods=["GET"])
@jwt_required()
def get_all_owned():
    player_id = get_jwt_identity()
    try:
        session = SessionLocal()

        pokemon_owned_json = []
        all_pokemon_owned = (
            session.query(PokemonOwned, PokemonStat.name)
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .filter(PokemonOwned.player_id == player_id)
            .all()
        )

        if not all_pokemon_owned:
            raise ValueError("No pokemon owned")

        for data, name in all_pokemon_owned:
            pokemon_owned_json.append(
                {
                    "name": name,
                    "id": data.id,
                    "player_id": data.player_id,
                    "pokedex_number": data.pokedex_number,
                    "in_team": data.in_team,
                    "obtained_at": data.obtained_at,
                    "mote": data.mote,
                }
            )

        return jsonify(pokemon_owned_json), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


@pokemon_owned.route("/pokemon/change_mote", methods=["PUT"])
@jwt_required()
def change_mote():
    try:
        data = request.get_json()

        player_id = get_jwt_identity()
        owned_pokemon_id = data.get("pokemon_id")
        mote = data.get("mote")

        if not owned_pokemon_id or not mote:
            raise ValueError("Missing data")

        session = SessionLocal()

        pokemon_data = (
            session.query(PokemonOwned)
            .filter(PokemonOwned.id == owned_pokemon_id)
            .first()
        )

        if pokemon_data.player_id != player_id:
            raise ValueError("This pokemon is not yours")

        pokemon_data.mote = mote

        session.commit()

        return jsonify({"message": "Changed mote"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500
