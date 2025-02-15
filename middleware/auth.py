from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request,get_jwt, unset_jwt_cookies
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

jwt = JWTManager()

def init_auth(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
    jwt.init_app(app)

def generate_token(user_id, role):
    return create_access_token(identity=str(user_id), additional_claims={"role": role})

def verify_token():
    try:
        verify_jwt_in_request()
        user_identity = get_jwt_identity()
        claims = get_jwt()
        role = claims.get("role", None)
        return {"id": user_identity, "role": role} if user_identity else None
    except Exception as e:
        return None

def logout_user():
    try:
        unset_jwt_cookies()
        return {"message": "Token supprimé avec succès"}
    except Exception as e:
        print("############################## ERROR ##############################")
        print(e)
        print("############################## ERROR ##############################")
        return {"error": "Erreur lors de la suppression du token"}