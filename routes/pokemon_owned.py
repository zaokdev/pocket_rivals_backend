from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from config.db import SessionLocal
from models.models import Player, PokemonOwned, PokemonStat


pokemon_owned = Blueprint("pokemon_owned", __name__)


# Usuario loggeado
@pokemon_owned.route("/pokemon/users_pokemon", methods=["GET"])
@jwt_required()
def get_all_owned():
    player_id = get_jwt_identity()
    try:
        session = SessionLocal()

        pokemon_owned_json = []
        all_pokemon_owned = (
            session.query(PokemonOwned, PokemonStat)
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .filter(PokemonOwned.player_id == player_id)
            .order_by(PokemonOwned.obtained_at.desc())
            .all()
        )

        if not all_pokemon_owned:
            raise ValueError("No pokemon owned")

        for data, stats in all_pokemon_owned:
            pokemon_owned_json.append(
                {
                    "name": stats.name,
                    "id": data.id,
                    "player_id": data.player_id,
                    "pokedex_number": data.pokedex_number,
                    "in_team": data.in_team,
                    "obtained_at": data.obtained_at,
                    "mote": data.mote,
                    "type1": stats.type1,
                }
            )

        return jsonify(pokemon_owned_json), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


@pokemon_owned.route(
    "/pokemon/users_pokemon/<string:owned_pokemon_id>", methods=["GET"]
)
@jwt_required()
def get_my_pokemon(owned_pokemon_id):
    try:
        player_id = get_jwt_identity()
        session = SessionLocal()

        pokemon_entry = (
            session.query(PokemonOwned, PokemonStat.name)
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .filter(
                PokemonOwned.id == owned_pokemon_id, PokemonOwned.player_id == player_id
            )
            .first()
        )
        if not pokemon_entry:
            return (
                jsonify({"message": "Pokemon not found or doesn't belong to you"}),
                404,
            )

        data, name = pokemon_entry
        pokemon_json = {
            "id": data.id,
            "name": name,
            "player_id": data.player_id,
            "pokedex_number": data.pokedex_number,
            "in_team": data.in_team,
            "obtained_at": data.obtained_at,
            "mote": data.mote,
        }
        return jsonify(pokemon_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()


@pokemon_owned.route(
    "/pokemon/public_users_pokemon/<string:player_id>", methods=["GET"]
)
@jwt_required()
def other_player_pokemon(player_id):
    try:
        session = SessionLocal()

        all_pokemon = (
            session.query(
                PokemonOwned, PokemonStat.name, PokemonStat.type1, Player.username
            )
            .join(
                PokemonStat, PokemonStat.pokedex_number == PokemonOwned.pokedex_number
            )
            .join(Player, Player.id == PokemonOwned.player_id)
            .filter(PokemonOwned.player_id == player_id)
            .all()
        )
        if not all_pokemon:
            return (
                jsonify(
                    {"message": "This player is not your friend or has no Pokemon"}
                ),
                404,
            )

        all_pokemon_json = []
        for owned, name, type1, username in all_pokemon:
            all_pokemon_json.append(
                {
                    "id": owned.id,
                    "name": name,
                    "owner": username,
                    "type1": type1,
                    "pokedex_number": owned.pokedex_number,
                    "in_team": owned.in_team,
                    "obtained_at": owned.obtained_at,
                    "mote": owned.mote,
                }
            )
        return jsonify(all_pokemon_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()


@pokemon_owned.route("/pokemon/change_mote", methods=["PUT"])
@jwt_required()
def change_mote():
    session = SessionLocal()
    try:
        data = request.get_json()

        player_id = get_jwt_identity()
        owned_pokemon_id = data.get("pokemon_id")
        mote = data.get("mote")

        if not owned_pokemon_id or not mote:
            raise ValueError("Missing data")

        pokemon_data = (
            session.query(PokemonOwned)
            .filter(PokemonOwned.id == owned_pokemon_id)
            .first()
        )

        if pokemon_data.player_id != player_id:
            raise ValueError("Pokemon not found or doesn't belong to you")

        pokemon_data.mote = mote

        session.commit()
        return jsonify({"message": "Changed mote"}), 201

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        session.close()


@pokemon_owned.route("/pokemon/delete", methods=["DELETE"])
@jwt_required()
def transfer_to_box():
    try:
        data = request.get_json()
        pokemon_id = data.get("pokemon_id")
        player_id = get_jwt_identity()

        if not pokemon_id:
            return jsonify({"message": "Pokemon_id not valid"}), 406

        session = SessionLocal()

        players_pokemon = (
            session.query(PokemonOwned)
            .filter(PokemonOwned.id == pokemon_id, PokemonOwned.player_id == player_id)
            .first()
        )

        if not players_pokemon:
            return (
                jsonify({"message": "Pokemon not found or doesn't belong to you"}),
                404,
            )

        session.delete(players_pokemon)
        session.commit()

        return (
            jsonify(
                {
                    "message": f"Pokemon with id {pokemon_id} has been transferred to the box"
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()
