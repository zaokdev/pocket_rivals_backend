from flask import Flask
from dotenv import load_dotenv
from config.db import init_db
from flask_jwt_extended import JWTManager
from routes.friends import friends
from routes.pokemon_owned import pokemon_owned
from routes.players import player
from routes.capture import capture_pokemon
from routes.trade import trade

app = Flask(__name__)

jwt = JWTManager()

load_dotenv()

init_db(app)
jwt.init_app(app)

app.register_blueprint(player)
app.register_blueprint(capture_pokemon)
app.register_blueprint(pokemon_owned)
app.register_blueprint(friends)
app.register_blueprint(trade)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
