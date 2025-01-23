from flask import Flask
from flask_migrate import Migrate
from .config.config import Config
from .config.model import db

def create_app():
    app = Flask(__name__ , template_folder = 'view' , static_folder = 'static')

    # Chargement de la configuration
    app.config.from_object(Config)

    # Initialisation des extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Importer les routes
    from middleware.routes import main_bp
    app.register_blueprint(main_bp)

    return app