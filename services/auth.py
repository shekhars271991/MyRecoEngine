import jwt
from flask import request, jsonify
from models import User
from redis_client import redis_client
from functools import wraps

SECRET_KEY = 'your_secret_key'

# Function to authenticate user and return JWT token
def authenticate_user(username, password):
    stored_password = redis_client.hget(f"user:{username}", "password")
    if stored_password and stored_password.decode('utf-8') == password:
        token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
        return token
    return None

# Login required decorator
def login_required(f):
    @wraps(f)  # This preserves the original function name
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user = User(username=data['username'])
                return f(user, *args, **kwargs)
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 403
        return jsonify({'message': 'Authorization required'}), 401
    return decorated_function
