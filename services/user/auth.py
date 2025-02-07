import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

MIDDLEWARE_URL = "http://localhost:5000" 


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("login")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Email ou mot de passe incorrect"}), 401
    
    response = requests.post(f"{MIDDLEWARE_URL}/generate_token", json={"id": user.id, "role": user.role_id})

    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({"error": "Erreur lors de la génération du token"}), 500
