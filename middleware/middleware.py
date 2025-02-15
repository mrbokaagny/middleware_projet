from prometheus_client import Counter, generate_latest
from flask import Flask, request, jsonify, Response
import requests
from auth import init_auth, verify_token, generate_token, logout_user
from logger import log_request
import json

app = Flask(__name__)
init_auth(app)  # Initialise JWT

# Définition des services disponibles
SERVICES = {
    "users": "http://localhost:5001",
    "products": "http://localhost:5002"
}

# Définition d'un compteur de requêtes
REQUEST_COUNT = Counter('request_count', 'Nombre de requêtes reçues', ['service', 'method'])

@app.before_request
def count_requests():
    REQUEST_COUNT.labels(service=request.path.split('/')[1], method=request.method).inc()

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Token supprimé avec succès"}), 200

@app.route('/generate_token', methods=['POST'])
def generate_token_route():

    data = request.get_json()
    user_id = data.get("id")
    role = data.get("role")

    if not user_id or not role:
        return jsonify({"error": "Données manquantes"}), 400

    token = generate_token(user_id, role)
    return jsonify({"access_token": token})

@app.route('/<service>/<path:endpoint>', methods=["GET", "POST", "PUT", "DELETE"])
def route_request(service, endpoint):
    """ Middleware qui redirige les requêtes vers les services correspondants. """

    # Vérifier si le service existe
    if service not in SERVICES:
        return jsonify({"error": "Service inconnu"}), 404
    
    user = None

    # Vérifier l'authentification sauf pour /login
    if not (service == "users" and endpoint == "login"):
        user = verify_token()
        if not user:
            return jsonify({"error": "Token invalide ou manquant"}), 401

    # Construire l'URL du service cible
    url = f"{SERVICES[service]}/{endpoint}"

    # Transférer la requête
    try:

        headers={key: value for key, value in request.headers if key != "Host"}

        if user:
            headers["user"] = json.dumps(user)

        response = requests.request(
            method=request.method,
            url=url,
            headers= headers,
            json=request.get_json() if request.method in ["POST", "PUT"] else None
        )

        log_request(service, endpoint, request.method, response.status_code)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Le service {service} est indisponible"}), 503

if __name__ == "__main__":
    app.run(port=5000, debug=True)
