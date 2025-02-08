import requests
from flask import Blueprint, render_template , request, redirect , url_for, flash, jsonify

main_bp = Blueprint("main", __name__)

BASE_URL = "http://localhost:5000"

@main_bp.route('/')
def index():
    return render_template('auth.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('home.html')

@main_bp.route('/products')
def product_list():
    products = []

    response = requests.get(f"{BASE_URL}/products/listing")

    if response.status_code == 200:
        data = response.json()
        products = data["products"]
        return render_template('product.html', products=products)
    else:
        flash("Une erreur s'est produite lors de la récupération des produits", "error")

@main_bp.route('/users')
def user_list():

    roles = []
    users = []

    response = requests.get(f"{BASE_URL}/users/listing")

    if response.status_code == 200:
        data = response.json()
        roles = data["roles"]
        users = data["users"]
        return render_template('user.html', roles=roles, users=users)
    else:
        flash("Une erreur s'est produite lors de la récupération des utilisateurs", "error")
    
    return render_template('user.html', roles=roles, users=users)


@main_bp.route('/user/update', methods=['POST'])
def modify_user():
    
    data = request.form

    required_fields = ['name', 'surname', 'email', 'role_id','user_id']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.user_list'))
    
    name = data['name']
    surname = data['surname']
    email = data['email']
    role_id = data['role_id']
    id = data['user_id']

    data = {
        "name": name,
        "surname": surname,
        "email": email,
        "role_id": role_id,
        "id": id
    }

    response = requests.put(f"{BASE_URL}/users/{id}", json=data)

    if response.status_code == 200:
        flash("Utilisateur mis à jour avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la modification de l'utilisateur", "error")

    return redirect(url_for('main.user_list'))

@main_bp.route('/user/<int:id>', methods=['GET'])
def user_detail(id):

    response = requests.get(f"{BASE_URL}/users/{id}")

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        flash("Une erreur s'est produite lors de la récupération de l'utilisateur", "error")
    
    return redirect(url_for('main.user_list'))


@main_bp.route('/user/create', methods=['POST'])
def insert_user():
    
    data = request.form

    required_fields = ['name', 'surname', 'email', 'role_id']

    if not all(field in data for field in required_fields):
        flash("Certaines informations n'ont pas été renseignées", "error")
        return redirect(url_for('main.user_list'))
    
    name = data['name']
    surname = data['surname']
    email = data['email']
    role_id = data['role_id']
    password = "bonjour"

    data = {
        "name": name,
        "surname": surname,
        "email": email,
        "role_id": role_id,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/users/created", json=data)

    if response.status_code == 201:
        flash("Utilisateur créé avec succès !", "success")
        return redirect(url_for('main.user_list'))
    else:
        flash("Une erreur s'est produite lors de la création de l'utilisateur", "error")
        return redirect(url_for('main.user_list'))

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

    data = {
        "name": name,
        "description": description,
        "price": price,
        "stock": quantity
    }

    response = requests.post(f"{BASE_URL}/products/created", json=data)

    if response.status_code == 201:
        flash("Produit créé avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la création du produit", "error")

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

    data = {
        "name": name,
        "description": description,
        "price": price,
        "stock": quantity
    }

    print(data)

    response = requests.put(f"{BASE_URL}/products/{id}", json=data)

    print(response)

    if response.status_code == 200:
        flash("Produit mis à jour avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la modification du produit", "error")

    return redirect(url_for('main.product_list'))

@main_bp.route('/product/<int:id>', methods=['GET'])
def product_detail(id):

    response = requests.get(f"{BASE_URL}/products/{id}")

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        flash("Une erreur s'est produite lors de la récupération du produit", "error")
    
    return redirect(url_for('main.product_list'))