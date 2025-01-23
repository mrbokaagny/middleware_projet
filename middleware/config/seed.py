import sys
import os

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from middleware import create_app
from middleware.config.model import db
from middleware.config.model import Role, Permission

app = create_app()

def seed_roles_and_permissions():

    roles_data = [
        {"name": "admin"},
        {"name": "accountant"},
        {"name": "manager"}
    ]

    permissions_data = [
        {"name": "all_rights", "description": "Tous les droits"},
        {"name": "finance_manager", "description": "Gestion des financers"},
        {"name": "product_manager", "description": "Gestion des produits"}

    ]

    with app.app_context():

        # Ajouter des rôles s'ils n'existent pas déjà
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data["name"]).first()
            if not role:
                role = Role(name=role_data["name"])
                db.session.add(role)

        # Ajouter des permissions s'ils n'existent pas déjà
        for perm_data in permissions_data:
            permission = Permission.query.filter_by(name=perm_data["name"]).first()
            if not permission:
                permission = Permission(name=perm_data["name"], description=perm_data["description"])
                db.session.add(permission)

        db.session.commit()

        print("Seeding complet : Roles et Permissions ont été créés")

# Lancer le seeding
if __name__ == "__main__":
    seed_roles_and_permissions()