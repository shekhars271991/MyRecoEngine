# routes_users.py

from flask import Blueprint, request, jsonify
from services.auth import authenticate_user, register_user, login_required
from models.User import User
import re
from services.db.redis_service import getJson
from services.movies.user_based_recommender import get_similar_users_profile

users_routes = Blueprint('users_routes', __name__, url_prefix='/user')

# User Registration Route
@users_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    
    # Input validation
    if not name or not username or not password:
        return jsonify({'message': 'All fields are required'}), 400

    # Validate username (e.g., alphanumeric, min length)
    if not re.match(r'^\w{3,}$', username):
        return jsonify({'message': 'Invalid username format'}), 400

    # Validate password length
    if len(password) < 6:
        return jsonify({'message': 'Password must be at least 6 characters long'}), 400

    if register_user(name, username, password):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'User already exists or invalid data'}), 400

# User Login Route
@users_routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token = authenticate_user(username, password)
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401




