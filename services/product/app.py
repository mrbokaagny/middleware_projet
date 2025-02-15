from prometheus_client import Counter, generate_latest
from flask import Flask, request, jsonify, Response
from config import Config
from extensions import db, jwt
from flask_migrate import Migrate

REQUEST_COUNT = Counter('request_count', 'Nombre de requêtes reçues', ['method'])



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    from routes import product_bp  
    app.register_blueprint(product_bp)

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
    app.run(port=5002, debug=True)
