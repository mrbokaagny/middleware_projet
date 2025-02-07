from flask import Flask, render_template
from init import create_app


app = create_app()

if __name__ == '__main__':
    app.secret_key = "app.config"
    app.run(port=5003,debug=True)