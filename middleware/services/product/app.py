from middleware.config.model import db , Product
from sqlalchemy import or_




def create_product(name, description, price, quantity):
    # Vérifier que le nom d'utilisateur n'existe pas déjà
    product = Product.query.filter_by(name=name).first()
    if product:
        return False, "Le nom du produit existe déjà"

    product = Product(name=name, description=description, price=price, quantity=quantity)

    try:
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        return False, "Une erreur est survenue lors de la création du produit"

    return True, "Produit créé avec succès"

def get_product_by_id(id):

    product = Product.query.filter_by(id=id).first()

    if not product:
        return False, "Le produit n'existe pas"

    return product, None

def get_products():
    products = Product.query.all()
    return products, None

def update_product(id, name, description, price, quantity):

    product = Product.query.filter_by(id=id).first()

    if not product:
        return False, "Le produit n'existe pas"
    
    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    try:
        db.session.commit()
    except Exception as e:
        return False, "Une erreur est survenue lors de la mise à jour du produit"

    return True, "Produit mis à jour avec succès"