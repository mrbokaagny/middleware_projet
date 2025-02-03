from flask import Blueprint, render_template , request, redirect , url_for, flash, jsonify
from middleware.config.model import db , Role , Permission , User
from middleware.services.users.app import create_user, get_user_by_id, update_user

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template('auth/auth.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('app/home.html')

@main_bp.route('/products')
def product_list():
    return render_template('app/product.html')

@main_bp.route('/users')
def user_list():
    roles = Role.query.with_entities(Role.id, Role.name).all()
    users = User.query.with_entities(User.id, User.name, User.surname, User.email, User.number, User.role_id).all()
    return render_template('app/user.html', roles=roles, users=users)

@main_bp.route('/user/update', methods=['POST'])
def modify_user():
    
    data = request.form

    required_fields = ['name', 'surname', 'email', 'number', 'role_id','user_id']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.user_list'))
    
    name = data['name']
    surname = data['surname']
    email = data['email']
    number = data['number']
    role_id = data['role_id']
    id = data['user_id']

    success, message = update_user(id, name, surname, email, number, role_id)

    if not success:
        flash(message, "error")
        return redirect(url_for('main.user_list'))

    flash("Utilisateur mis à jour avec succès !", "success")
    return redirect(url_for('main.user_list'))

@main_bp.route('/user/<int:id>', methods=['GET'])
def user_detail(id):

    user, message = get_user_by_id(id)

    if not user:
        flash(message, "error")
        return redirect(url_for('main.user_list'))

    return jsonify(user.to_dict())

@main_bp.route('/user/create', methods=['POST'])
def insert_user():
    
    data = request.form

    required_fields = ['name', 'surname', 'email', 'number', 'role_id']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.user_list'))
    
    name = data['name']
    surname = data['surname']
    email = data['email']
    number = data['number']
    role_id = data['role_id']
    password = "bonjour"

    success, message = create_user(name, surname, email, number, password, role_id)

    if not success:
        flash(message, "error")
        return redirect(url_for('main.user_list'))

    flash("Utilisateur créé avec succès !", "success")
    return redirect(url_for('main.user_list'))

