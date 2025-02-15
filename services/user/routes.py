from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Role
import json
from sqlalchemy.orm import joinedload

user_bp = Blueprint('user', __name__)

@user_bp.route('/listing', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    roles = Role.query.all()
    roles_list = [{"id": r.id, "name": r.name} for r in roles]
    users_list = [{"id": u.id, "name": u.name, "surname": u.surname, "email": u.email, "role": u.role_id} for u in users]
    return jsonify({"users": users_list , "roles": roles_list})

@user_bp.route('/created', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user["role"] != 1: 
        print("permission refusée")
        return jsonify({"error": "Permission refusée"}), 403

    data = request.get_json()
    new_user = User(name=data['name'], surname=data['surname'], email=data['email'], role_id=data['role_id'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):

    user = User.query.get_or_404(user_id)
    if user :
        user_data = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "role_id": user.role_id
        }
        #user = User(name=user['name'], surname=user['surname'], email=user['email'], role_id=user['role_id'])
    return jsonify(user_data)


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):

    data = request.get_json()
    user = User.query.get_or_404(user_id)
    if user :
        user.name = data['name']
        user.surname = data['surname']
        user.email = data['email']
        user.role_id = data['role_id']
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour avec succès"}), 200
    else:  
        return jsonify({"message": "Utilisateur non trouvé"}), 404


@user_bp.route('/profil', methods=['GET'])
@jwt_required()
def get_user_profile():

    user = request.headers.get('user')
    user = json.loads(user)
    print("############################## USER ##############################")
    print(user)
    print("############################## USER ##############################")

    if user:
        user = User.query.options(joinedload(User.role)).filter_by(id=user['id']).first()
        if user:
            user_data = {
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "email": user.email,
            "role": user.role.name
            }
            
            return jsonify(user_data)
        else:
            return jsonify({"message": "Utilisateur non trouvé"}), 404
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404