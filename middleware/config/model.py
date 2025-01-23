from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Table d'association pour la relation Many-to-Many entre Role et Permission
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class BaseModel(db.Model):
    __abstract__ = True  

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    number = db.Column(db.String(50), nullable=False)

    # Relation avec Role (Many-to-One)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='users')  # Un utilisateur peut avoir un seul rôle

    def __repr__(self):
        return f"User('{self.name}', '{self.surname}', '{self.email}', '{self.number}')"


class Role(BaseModel):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relation Many-to-Many avec Permission
    permissions = db.relationship(
        'Permission',
        secondary=role_permissions,
        backref=db.backref('roles', lazy='dynamic')
    )

    def __repr__(self):
        return f"Role(id={self.id}, name='{self.name}')"


class Permission(BaseModel):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Permission('{self.name}', '{self.description}')"
