from flask import Blueprint, render_template , request, redirect , url_for
from middleware.config.model import db , Role , Permission , User

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template('auth/auth.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('app/home.html')

@main_bp.route('/users')
def users_list():
    roles = Role.query.with_entities(Role.id, Role.name).all()
    users = User.query.with_entities(User.id, User.name, User.surname, User.email, User.number, User.role_id).all()
    return render_template('app/user.html', roles=roles, users=users)


@main_bp.route('/users/create', methods=['POST'])
def create_user():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    number = request.form['number']
    role_id = request.form['role_id']
    password = request.form['number']

    # Vérifier que le rôle existe
    role = Role.query.filter_by(id=role_id).first()
    if not role:
        return "Le rôle n'existe pas"

    # Vérifier que le nom d'utilisateur n'existe pas déjà
    user = User.query.filter_by(email=email,number=number).first()
    if user:
        return "L'email ou le numéro d'utilisateur existe déjà"
    
    user = User(name=name, surname=surname, email=email, number=number, password=password, role_id=role_id)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('main.users_list'))

