from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from sqlalchemy import func, or_
from helpers.helpers import choose_capture_rate, create_id
from models.models import Player, PokemonOwned, PokemonStat
from config.db import SessionLocal
from flask_jwt_extended import jwt_required, get_jwt_identity
import random
from datetime import datetime

capture_pokemon = Blueprint("capture_pokemon", __name__)

bcrypt = Bcrypt()


# Capturar Pokemon aleatorio
@capture_pokemon.route("/capture_pokemon", methods=["GET"])
@jwt_required()
def get_a_pokemon():
    try:
        player_id = get_jwt_identity()
        session = SessionLocal()

        # Esto es para lo de verificar si ya hizo un lanzamiento antes de las horas
        # session.query(Player.last_opened).filter(Player.id == player_id).first()

        capture_rates = (
            session.query(
                PokemonStat.capture_rate, func.count(PokemonStat.capture_rate)
            )
            .group_by(PokemonStat.capture_rate)
            .order_by(func.count(PokemonStat.capture_rate))
        ).all()

        if not capture_rates:
            raise ValueError("Problem")

        choosen = choose_capture_rate(dict(capture_rates))

        print("CAPTURE RATE ELEGIDO: " + str(choosen))

        pokemon_list = (
            session.query(PokemonStat.pokedex_number)
            .filter(PokemonStat.capture_rate == choosen)
            .all()
        )

        print(pokemon_list)
        pokedex_numbers = []
        for pokemon_tuple in pokemon_list:
            pokedex_numbers.append(pokemon_tuple[0])

        final_pokedex_number = random.choice(pokedex_numbers)

        final_pokemon = (
            session.query(PokemonStat)
            .filter(PokemonStat.pokedex_number == final_pokedex_number)
            .first()
        )

        owned_pokemon_id = create_id(24)
        message = f"You've captured {final_pokemon.name}"

        owned_pokemon_data = PokemonOwned(
            id=owned_pokemon_id,
            player_id=player_id,
            pokedex_number=final_pokedex_number,
            obtained_at=datetime.now(),
            in_team=False,
        )

        session.add(owned_pokemon_data)
        session.commit()

        return (
            jsonify(
                {
                    "message": message,
                    "pokedex_number": final_pokedex_number,
                    "name": final_pokemon.name,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"message": str(e)}), 500

    finally:
        session.close()
