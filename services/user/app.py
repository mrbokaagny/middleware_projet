from prometheus_client import Counter, generate_latest
from flask import Flask, request, jsonify, Response
from config import Config
from flask_migrate import Migrate
from extensions import db, jwt, bcrypt

REQUEST_COUNT = Counter('request_count', 'Nombre de requêtes reçues', ['method'])



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    from auth import auth_bp  
    from routes import user_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    @app.before_request
    def restrict_access():
        allowed_origin = "http://localhost:5000"
        if request.referrer and not request.referrer.startswith(allowed_origin):
            return jsonify({"error": "Accès interdit"}), 403
    
    @app.before_request
    def count_requests():
        REQUEST_COUNT.labels(method=request.method).inc()

    @app.route('/metrics', methods=['GET'])
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5001, debug=True)
