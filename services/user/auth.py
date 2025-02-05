from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401

    token = create_access_token(identity={"id": user.id, "role": user.role_id})
    return jsonify({"access_token": token})
