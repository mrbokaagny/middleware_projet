from prometheus_client import Counter, generate_latest
from flask import Flask, render_template, Response, request
from init import create_app

app = create_app()

REQUEST_COUNT = Counter('request_count', 'Nombre de requêtes reçues', ['method'])

@app.before_request
def count_requests():
    REQUEST_COUNT.labels(method=request.method).inc()

@app.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


if __name__ == '__main__':
    app.secret_key = "app.config"
    app.run(port=5003,debug=True)