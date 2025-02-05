from models import Role
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


if __name__ == "__main__":
    seed()