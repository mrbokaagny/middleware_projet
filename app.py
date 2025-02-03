from flask import Flask, render_template
from middleware import create_app


app = create_app()

if __name__ == '__main__':
    app.secret_key = "super_secret_key" 
    app.run(debug=True)