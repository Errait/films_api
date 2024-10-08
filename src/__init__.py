from flask import Flask, request, session, flash, redirect, url_for, render_template
import flask
import logging
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask tutorial'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('index.html')


@app.route('/greeting', methods=['POST'])
def greeting():
    name = flask.request.form.get('name')
    if not name:
        return 'Please, enter a value', 400
    return flask.render_template('greeting.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if models.User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        new_user = models.User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = models.User.query.filter_by(username=username).first()
        print(f"User: {user}")
        print(f"Provided password: {password}")

        if user:
            print(f"Hashed password in DB: {user.password_hash}")
            print(f"Password check result: {user.check_password(password)}")

        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

        session['username'] = user.username
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    user = models.User.query.filter_by(username=username).first()

    return f'Hello, {user.username}! Welcome to your dashboard.'


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


app.debug = True

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@app.after_request
def sql_debug(response):
    return response


if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(rule)



from src import routes
from src.database import models