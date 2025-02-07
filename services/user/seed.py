from models import Role, User
from app import create_app
from extensions import db




def seed():

    roles = [
        'admin',
        'shelving technician',
        'accountant',
        'cashier',
    ]

    app = create_app()

    with app.app_context():

        for name in roles:
            role = Role.query.filter_by(name=name).first()
            if not role:
                db.session.add(Role(name=name))

        db.session.commit()


        users = [
            {
                "name": "Boka",
                "surname": "Agny Ble Romaric-Rocephin",
                "email": "agny.boka@stock.com",
                "password": "admin",
                "role_id": 2,
            }
        ]

        for user_data in users:

            existing_user = User.query.filter_by(email=user_data["email"]).first()
            if not existing_user:
                user = User(
                    name=user_data["name"],
                    surname=user_data["surname"],
                    email=user_data["email"],
                    role_id=user_data["role_id"]
                )
                user.set_password(user_data["password"])  
                db.session.add(user)

        db.session.commit() 


if __name__ == "__main__":
    seed()