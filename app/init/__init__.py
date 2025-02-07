from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__ , template_folder = '../view' , static_folder = '../static')

    # Chargement de la configuration
    app.config.from_object(Config)

    # Importer les routes
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app