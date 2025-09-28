from flask import Blueprint, jsonify, request
from app.models.mongo.trade import Trade
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

trade_bp: Blueprint = Blueprint("trade_bp", __name__)


@trade_bp.route("/trades/<friend_id>", methods=["GET"])
@jwt_required()
def get_requests_specific(friend_id: str):
    trainer_id: str = get_jwt_identity()
    pending: list | None = Trade.get_pending_trades_specific(trainer_id, friend_id)
    return jsonify({"trades": pending}), 200


@trade_bp.route("/trades/make", methods=["POST"])
@jwt_required()
def request_pokemon():
    trainer_id: str = get_jwt_identity()
    datax: dict = request.get_json()
    friend_id: str | None = datax.get("friend_id")
    pkm_traded: int | None = datax.get("pkm_traded")
    pkm_received: int | None = datax.get("pkm_received")
    data: dict = {
        "trainer_id": trainer_id,
        "friend_id": friend_id,
        "pkm_traded": pkm_traded,
        "pkm_received": pkm_received,
        "trade_status": "pending",
    }
    result: bool = Trade.request_trade(data)
    return jsonify({"message": "Action completed", "success": result}), 200


@trade_bp.route("/trades/confirm", methods=["PUT"])
@jwt_required()
def confirm_request():
    data: dict = request.get_json()
    result: bool = Trade.confirm_trade(data)
    return jsonify({"message": "Action completed", "success": result}), 200


@trade_bp.route("/trades/deny", methods=["PUT"])
@jwt_required()
def deny_request():
    data: dict = request.get_json()
    result: bool = Trade.deny_trade(data)
    return jsonify({"message": "Action completed", "success": result}), 200
