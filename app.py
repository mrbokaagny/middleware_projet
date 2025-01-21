from flask import Flask, render_template

app = Flask(__name__ , template_folder = 'middleware/view' , static_folder = 'middleware/static')

@app.route('/')
def index():
    return render_template('auth/auth.html')

@app.route('/dashboard')
def dashboard():
    return render_template('app/home.html')

if __name__ == '__main__':
    app.run(debug=True)