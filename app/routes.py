import requests
from flask import Blueprint, render_template , request, redirect , url_for, flash, jsonify, session

main_bp = Blueprint("main", __name__)

BASE_URL = "http://localhost:5000"

@main_bp.route('/')
def index():
    return render_template('auth.html')

@main_bp.route('/dashboard')
def dashboard():

    user = None

    if not session.get('access_token'):
        flash("Vous n'êtes pas connecté", "error")
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get(f"{BASE_URL}/users/profil", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("############################## DATA ##############################")
        user = data
        print("############################## DATA ##############################")
    else:
        flash("Une erreur s'est produite lors de la récupération de l'utilisateur", "error")
        return redirect(url_for('main.index'))

    return render_template('home.html' , user=user)

@main_bp.route('/products')
def product_list():
    products = []

    try : 

        if not session.get('access_token'):
            return redirect(url_for('main.index'))
    
        headers = {"Authorization": f"Bearer {session['access_token']}"}

        response = requests.get(f"{BASE_URL}/products/listing", headers=headers)

        if response.status_code == 200:
            data = response.json()
            products = data["products"]
            return render_template('product.html', products=products)
        elif response.status_code == 401:
            flash("Vous n'êtes pas connecté", "error")
            return redirect(url_for('main.index'))
        else:
            flash("Une erreur s'est produite lors de la récupération des produits", "error")
    except Exception as e:
        print(e)
        flash("Une erreur s'est produite lors de la récupération des produits", "error")
        return redirect(url_for('main.index'))

@main_bp.route('/users')
def user_list():

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    roles = []
    users = []

    response = requests.get(f"{BASE_URL}/users/listing", headers=headers)

    if response.status_code == 200:
        data = response.json()
        roles = data["roles"]
        users = data["users"]
        return render_template('user.html', roles=roles, users=users)
    elif response.status_code == 401:
        flash("Vous n'êtes pas connecté", "error")
        return redirect(url_for('main.index'))
    else:
        flash("Une erreur s'est produite lors de la récupération des utilisateurs", "error")
    
    return render_template('user.html', roles=roles, users=users)


@main_bp.route('/user/update', methods=['POST'])
def modify_user():

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
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

    response = requests.put(f"{BASE_URL}/users/{id}", json=data , headers=headers)

    if response.status_code == 200:
        flash("Utilisateur mis à jour avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la modification de l'utilisateur", "error")

    return redirect(url_for('main.user_list'))

@main_bp.route('/user/<int:id>', methods=['GET'])
def user_detail(id):

    if not session.get('access_token'):
        return redirect(url_for('main.index'))

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    response = requests.get(f"{BASE_URL}/users/{id}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        flash("Une erreur s'est produite lors de la récupération de l'utilisateur", "error")
    
    return redirect(url_for('main.user_list'))


@main_bp.route('/user/create', methods=['POST'])
def insert_user():

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
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

    response = requests.post(f"{BASE_URL}/users/created", json=data, headers=headers)

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

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
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

    response = requests.post(f"{BASE_URL}/products/created", json=data, headers=headers)

    if response.status_code == 201:
        flash("Produit créé avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la création du produit", "error")

    return redirect(url_for('main.product_list'))

@main_bp.route('/product/update', methods=['POST'])
def modify_product():

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    
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

    response = requests.put(f"{BASE_URL}/products/{id}", json=data, headers=headers)

    print(response)

    if response.status_code == 200:
        flash("Produit mis à jour avec succès !", "success")
    else:
        flash("Une erreur s'est produite lors de la modification du produit", "error")

    return redirect(url_for('main.product_list'))

@main_bp.route('/product/<int:id>', methods=['GET'])
def product_detail(id):

    if not session.get('access_token'):
        return redirect(url_for('main.index'))
    
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    response = requests.get(f"{BASE_URL}/products/{id}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        flash("Une erreur s'est produite lors de la récupération du produit", "error")
    
    return redirect(url_for('main.product_list'))


############################# AUTHENTIFICATION ##############################

@main_bp.route('/auth', methods=['POST'])
def auth():

    data = request.form

    username = data["username"]
    password = data["password"]

    if not username or not password:
        flash("Vous devez renseigner votre identifiant et votre mot de passe", "error")
        return redirect(url_for('main.index'))

    response = requests.post(f"{BASE_URL}/users/login", json={"login": username, "password": password})

    if response.status_code == 200:
        data = response.json()
        print("############################## TOKEN ##############################")
        print(data['access_token'])
        session['access_token'] = data['access_token']
        print("############################## TOKEN ##############################")
        return redirect(url_for('main.dashboard'))
    else:
        flash("Vos identifiants ne correspondent pas à nos enregistrements", "error")
        return redirect(url_for('main.index'))

@main_bp.route('/logout', methods=['GET'])
def logout():

    try : 
        
        if not session.get('access_token'):
            return redirect(url_for('main.index'))
    
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        
        response = requests.post(f"{BASE_URL}/users/logout", headers=headers)

        if response.status_code == 200:
            return redirect(url_for('main.index'))
        else:
            flash("Une erreur s'est produite lors de la récupération de l'utilisateur", "error")
            return redirect(url_for('main.index'))
    except Exception as e:
        print("############################## ERROR ##############################")
        print(e)
        print("############################## ERROR ##############################")
        flash("Une erreur s'est produite lors de la récupération de l'utilisateur", "error")
        return redirect(url_for('main.index'))