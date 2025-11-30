from flask import request
from extensions import socketio

connected_users = {}


@socketio.on("connect")
def handle_connect():
    print("Cliente conectado:", request.sid)


@socketio.on("connect_user")
def connect_user(data):
    user_id = data.get("user_id")
    sid = request.sid

    connected_users[user_id] = sid
    print(f"Usuario {user_id} asociado al SID {sid}")


@socketio.on("disconnect")
def disconnect_user():
    sid = request.sid
    for uid, stored_sid in list(connected_users.items()):
        if stored_sid == sid:
            del connected_users[uid]
            print(f"Usuario {uid} desconectado")
            break
