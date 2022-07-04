from flask import Blueprint, jsonify, render_template, request, jsonify
from api.models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
import json
from os import path

baseDir = path.dirname(__file__)
auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder=path.join(baseDir, '../templates/auth'))

@auth.route('/login', methods=['GET'])
def load_login_page():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        exist_user = User.query.filter_by(username=username).first()
        resp = {}
        if exist_user is not None:
            if check_password_hash(exist_user.password, password):
                credentials = {'username': username, 'isAdmin': exist_user.isAdmin, 'id': exist_user.id}
                access_token = create_access_token(identity = credentials)
                refresh_token = create_refresh_token(identity = credentials)
                resp = {'status': 'success',
                        'access_token': access_token,
                        'refresh_token': refresh_token}
            else:
                resp = {'status': 'error', 'message': 'Wrong password!'}
        else:
            resp = {'status': 'error', 'message': 'user is non-exist'}
        return jsonify(resp), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500

@auth.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['username']
        password = request.form['password']

        if username is None or password is None:
            return jsonify({'status': 'error', 'message': 'username and password are required'})

        exist_user = User.query.filter_by(username=username).first()
        resp = {}
        if exist_user is None:
            hash_password = generate_password_hash(password)
            new_user = User(username = username, password = hash_password)
            db.session.add(new_user)
            db.session.commit()
            credentials = {'username': username, 'isAdmin': False, 'id': new_user.id}
            resp = {'status': 'success', 
                    'access_token': create_access_token(identity = credentials),
                    'refresh_token': create_refresh_token(identity = credentials)}
        else:
            resp = {'status': 'error', 'message': 'user existed!'}
        return jsonify(resp)
    except Exception as e:
        return jsonify({'status': 'error', 'message': e}), 500


    
    