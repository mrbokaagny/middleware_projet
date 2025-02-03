from middleware.config.model import db , Role , Permission , User
from sqlalchemy import or_



def create_user(name, surname, email, number, password, role_id):

    # Vérifier que le rôle existe
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return False, "Le rôle n'existe pas"

    # Vérifier que le nom d'utilisateur n'existe pas déjà
    user = User.query.filter(
        or_(User.email == email, User.number == number)
    ).first()
    if user:
        return False, "L'email ou le numéro est déjà utilisé"
    
    user = User(name=name, surname=surname, email=email, number=number, password=password, role_id=role_id)

    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return False, "Une erreur est survenue lors de la création de l'utilisateur"

    return True, "Utilisateur créé avec succès"

def get_user_by_id(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return False, "L'utilisateur n'existe pas"

    return user, None

def get_users():
    users = User.query.all()
    return users, None

def update_user(id, name, surname, email, number, role_id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return False, "L'utilisateur n'existe pas"
    
    user = User.query.filter(
        or_(User.email == email, User.number == number)
    ).first()

    user.name = name
    user.surname = surname
    user.email = email
    user.number = number
    user.role_id = role_id

    try:
        db.session.commit()
    except Exception as e:
        return False, "Une erreur est survenue lors de la mise à jour de l'utilisateur"

    return True, "Utilisateur mis à jour avec succès"

