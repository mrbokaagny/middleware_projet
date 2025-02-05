from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
import datetime

jwt = JWTManager()

def init_auth(app):
    app.config["JWT_SECRET_KEY"] = "super_secret_key"  # Change cette clé !
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
    jwt.init_app(app)

def generate_token(user_id, role):
    return create_access_token(identity={"id": user_id, "role": role})

def verify_token():
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception as e:
        return None