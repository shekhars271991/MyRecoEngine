import jwt
from flask import request, jsonify
from services.redis_service import redis_client
from models import User
from functools import wraps
import bcrypt

SECRET_KEY = 'your_secret_key'

# Register a new user with hashed password
def register_user(username, password):
    if redis_client.exists(f"user:{username}"):
        return False

    # Hash the password and store it as a byte string
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    redis_client.hset(f"user:{username}", "password", hashed_password)
    return True

def authenticate_user(username, password):
    stored_password = redis_client.hget(f"user:{username}", "password")
    
    # Debug: Print the stored password
    print(f"Stored password (bytes): {stored_password}")

    # bcrypt.checkpw expects a byte string for both the plain and hashed password
    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password):
        # Generate JWT token
        token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')

        # In some versions, `jwt.encode()` may return a byte string
        if isinstance(token, bytes):
            token = token.decode('utf-8')  # Ensure token is a string

        return token
    return None

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        # Check for Bearer prefix in the Authorization header
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]  # Extract the token part after 'Bearer '

            try:
                # Decode the token
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user = User(username=data['username'])
                return f(user, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 403
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 403
        return jsonify({'message': 'Authorization required'}), 401
    return decorated_function
