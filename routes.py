from flask import Blueprint, request, jsonify
from services.auth import authenticate_user, register_user, login_required
from models.User import User
from services.db.redis_service import getJson
import re

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    
    if not name or not username or not password:
        return jsonify({'message': 'All fields are required'}), 400

    if not re.match(r'^\w{3,}$', username):
        return jsonify({'message': 'Invalid username format'}), 400

    if len(password) < 4:
        return jsonify({'message': 'Password must be at least 6 characters long'}), 400

    if register_user(name, username, password):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'User already exists or invalid data'}), 400

@main_routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token = authenticate_user(username, password)
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@main_routes.route('/user/profile', methods=['GET'])
@login_required
def get_user_profile(user: User):
    try:
        userprofile_key = "profile:"+user.username
        profile = getJson(userprofile_key)
        if 'feature_weights' in profile:
            profile.pop('feature_weights')
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
