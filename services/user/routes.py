from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Role

user_bp = Blueprint('user', __name__)

@user_bp.route('/listing', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    users_list = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role_id} for u in users]
    return jsonify(users_list)

@user_bp.route('/created', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user["role"] != 1: 
        return jsonify({"error": "Permission refusée"}), 403

    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role_id=data['role_id'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201
