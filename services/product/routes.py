from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db  
from models import Product   

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    products_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]
    return jsonify(products_list)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user["role"] != 1:  # Seul l'admin (role_id = 1) peut ajouter un produit
        return jsonify({"error": "Permission refusée"}), 403

    data = request.get_json()
    new_product = Product(name=data['name'], description=data.get('description', ""), price=data['price'], stock=data['stock'])
    
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Produit ajouté avec succès"}), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    if current_user["role"] != 1:
        return jsonify({"error": "Permission refusée"}), 403

    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify({"message": "Produit mis à jour"}), 200

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user = get_jwt_identity()
    if current_user["role"] != 1:
        return jsonify({"error": "Permission refusée"}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Produit supprimé"}), 200
