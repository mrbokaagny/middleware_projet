from flask import Blueprint, render_template , request, redirect , url_for, flash, jsonify
from middleware.config.model import db , Role , Permission , User, Product
from middleware.services.users.app import create_user, get_user_by_id, update_user
from middleware.services.product.app import create_product, get_product_by_id, update_product

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return render_template('auth/auth.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('app/home.html')

@main_bp.route('/products')
def product_list():
    products = Product.query.with_entities(Product.id, Product.name, Product.description, Product.price, Product.quantity).all()
    return render_template('app/product.html', products=products)
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

############################# PRODUCTS ##############################
@main_bp.route('/product/create', methods=['POST'])
def insert_product():
    
    data = request.form

    required_fields = ['name', 'description', 'price', 'quantity']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.product_list'))
    
    name = data['name']
    description = data['description']
    price = data['price']
    quantity = data['quantity']

    success, message = create_product(name, description, price, quantity)

    if not success:
        flash(message, "error")
        return redirect(url_for('main.product_list'))

    flash("Produit créé avec succès !", "success")
    return redirect(url_for('main.product_list'))

@main_bp.route('/product/update', methods=['POST'])
def modify_product():
    
    data = request.form

    required_fields = ['name', 'description', 'price', 'quantity']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.product_list'))
    
    name = data['name']
    description = data['description']
    price = data['price']
    quantity = data['quantity']
    id = data['product_id']

    success, message = update_product(id, name, description, price, quantity)

    if not success:
        flash(message, "error")
        return redirect(url_for('main.product_list'))

    flash("Produit mis à jour avec succès !", "success")
    return redirect(url_for('main.product_list'))

@main_bp.route('/product/<int:id>', methods=['GET'])
def product_detail(id):

    product, message = get_product_by_id(id)

    if not product:
        flash(message, "error")
        return redirect(url_for('main.product_list'))

    return jsonify(product.to_dict())