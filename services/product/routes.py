from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db  
from models import Product   

product_bp = Blueprint('product', __name__)

@product_bp.route('/listing', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    products_list = [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock, "description": p.description} for p in products]
    return jsonify({"products": products_list})

@product_bp.route('/created', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user["role"] != 1:  
        return jsonify({"error": "Permission refusée"}), 403

    data = request.get_json()
    new_product = Product(name=data['name'], description=data["description"], price=data['price'], stock=data['stock'])
    
    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Produit ajouté avec succès"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    if current_user["role"] != 1:
        return jsonify({"error": "Permission refusée"}), 403

    product = Product.query.get_or_404(product_id)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Données JSON manquantes"}), 400
    
    required_fields = ["name", "description", "price", "stock"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Champs manquants"}), 400

    if product : 

        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.stock = data['stock']

        try:
            db.session.commit()
            return jsonify({"message": "Produit mis à jour"}), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500
    else:  
        return jsonify({"message": "Produit non trouvé"}), 404


@product_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)

    if product:
        product_data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "description": product.description
        }
        return jsonify(product_data)
    else:    
        return jsonify({"message": "Produit non trouvé"}), 404