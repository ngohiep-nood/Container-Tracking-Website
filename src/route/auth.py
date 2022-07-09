from flask import Blueprint, jsonify, render_template, request, jsonify
from src.models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from src.schema.form_validation import RegistrationForm, LoginForm
import os
from os import path
from flasgger import swag_from

baseDir = path.dirname(__file__)
auth = Blueprint('auth', __name__, url_prefix='/auth',
                 template_folder=path.join(baseDir, '../templates/auth'))

@auth.route('/login', methods=['GET'])
@swag_from('../docs/auth/load_login_page.yaml')
def load_login_page():
    return render_template('login.html')

@auth.route('/register', methods=['GET'])
@swag_from('../docs/auth/load_register_page.yaml')
def load_register_page():
    return render_template('register.html')

@auth.route('/login', methods=['POST'])
@swag_from('../docs/auth/login.yaml')
def login():
    try:
        form = LoginForm(request.form)

        if not form.validate():
            return jsonify({'status': 'error', 'message': form.errors})
        username = request.form['username']
        password = request.form['password']
        exist_user = User.query.filter_by(username=username).first()
        resp = {}
        statusCode = 200
        if exist_user is not None:
            if check_password_hash(exist_user.password, password):
                credentials = {'username': username,
                               'isAdmin': exist_user.isAdmin, 'id': exist_user.id}
                access_token = create_access_token(identity=credentials)
                refresh_token = create_refresh_token(identity=credentials)
                resp = {'status': 'success',
                        'access_token': access_token,
                        'refresh_token': refresh_token}
            else:
                resp = {'status': 'error', 'message': {'password': ['wrong password!']}}
                statusCode = 401
        else:
            resp = {'status': 'error', 'message': {'username': ['username not found']}}
            statusCode = 404
        return jsonify(resp), statusCode
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@auth.route('/register', methods=['POST'])
@swag_from('../docs/auth/register.yaml')
def register():
    try:
        form = RegistrationForm(request.form)

        if not form.validate():
            return jsonify({'status': 'error', 'message': form.errors }), 401
        
        username = form.username.data
        password = form.password.data
        email = form.email.data
        secret_key = form.secret_key.data
        print(secret_key)
        exist_user = User.query.filter_by(username=username).first()
        resp = {}
        if exist_user is None:
            hash_password = generate_password_hash(password)
            isAdmin = False
            if secret_key is not None:
                if secret_key == os.environ.get('SECRET_KEY'):
                    isAdmin = True
                else:
                    return {
                        'status': 'error',
                        "message": "The secret key doesn't match"
                    }, 401
            new_user = User(username=username,
                            password=hash_password,
                            isAdmin=isAdmin,
                            email=email)
            db.session.add(new_user)
            db.session.commit()
            credentials = {'username': username,
                           'isAdmin': isAdmin, 'id': new_user.id}
            resp = {'status': 'success',
                    'access_token': create_access_token(identity=credentials),
                    'refresh_token': create_refresh_token(identity=credentials)}
        else:
            resp = {'status': 'error', 'message': {'username': ['username existed!']}}, 409
        return jsonify(resp)
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@auth.route('/token', methods=['GET'])
@jwt_required(refresh=True)
@swag_from('../docs/auth/token.yaml')
def get_access_token():
    try:
        identity = get_jwt_identity()
        return jsonify({
            'status': 'success',
            'access_token': create_access_token(identity=identity)
        })
    except Exception as e:
        jsonify({'status': 'error', 'message': e}), 500