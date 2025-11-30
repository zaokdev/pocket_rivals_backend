from flask import Flask
from dotenv import load_dotenv
from config.db import init_db
from routes.friends import friends
from routes.pokemon_owned import pokemon_owned
from routes.players import player
from routes.capture import capture_pokemon
from routes.trade import trade
from extensions import socketio, jwt

app = Flask(__name__)

load_dotenv()

init_db(app)
jwt.init_app(app)
socketio.init_app(app)

app.register_blueprint(player)
app.register_blueprint(capture_pokemon)
app.register_blueprint(pokemon_owned)
app.register_blueprint(friends)
app.register_blueprint(trade)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
