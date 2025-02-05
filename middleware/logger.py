import logging

# Configuration du logging
logging.basicConfig(filename="middleware.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_request(service, endpoint, method, status):
    logging.info(f"Service: {service}, Endpoint: {endpoint}, Méthode: {method}, Status: {status}")
