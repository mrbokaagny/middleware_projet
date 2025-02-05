from flask import Flask, request, jsonify
import requests
from auth import init_auth, verify_token
from logger import log_request

app = Flask(__name__)
init_auth(app)  # Initialise JWT

# Définition des services disponibles
SERVICES = {
    "users": "http://localhost:5001",
    "products": "http://localhost:5002"
}

@app.route('/<service>/<path:endpoint>', methods=["GET", "POST", "PUT", "DELETE"])
def route_request(service, endpoint):
    """ Middleware qui redirige les requêtes vers les services correspondants. """

    # Vérifier si le service existe
    if service not in SERVICES:
        return jsonify({"error": "Service inconnu"}), 404

    # Vérifier l'authentification sauf pour /login
    if not (service == "users" and endpoint == "login"):
        user = verify_token()
        if not user:
            return jsonify({"error": "Token invalide ou manquant"}), 401

    # Construire l'URL du service cible
    url = f"{SERVICES[service]}/{endpoint}"

    # Transférer la requête
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != "Host"},
            json=request.get_json() if request.method in ["POST", "PUT"] else None
        )

        log_request(service, endpoint, request.method, response.status_code)
        return jsonify(response.json()), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Le service {service} est indisponible"}), 503

if __name__ == "__main__":
    app.run(port=5000, debug=True)
