from flask import Blueprint, request, jsonify
from services.auth import authenticate_user, register_user, login_required
from services.recommender import get_recommendations
from models import Movie, User
import json
from redis_service import insert_movie_into_redis


main_routes = Blueprint('main_routes', __name__)

# User Registration Route
@main_routes.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if register_user(username, password):
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'User already exists or invalid data'}), 400

# User Login Route
@main_routes.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token = authenticate_user(username, password)
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Get Movie List Route (with descriptions and cast)
@main_routes.route('/movies', methods=['GET'])
@login_required
def get_movies(user):
    movies = Movie.get_all_movies()
    return jsonify(movies), 200
    # return jsonify([movie.serialize() for movie in movies]), 200

# User Action: Watched/Not Watched, Rating Route
@main_routes.route('/movies/action', methods=['POST'])
@login_required
def movie_action(user):
    movie_id = request.json.get('movie_id')
    watched = request.json.get('watched')
    rating = request.json.get('rating', None)
    
    user.update_movie_status(movie_id, watched, rating)
    return jsonify({'message': 'Action updated successfully'}), 200

# Get Recommendations Route
@main_routes.route('/movies/recommendations', methods=['GET'])
@login_required
def get_movie_recommendations(user):
    recommendations = get_recommendations(user)
    return jsonify(recommendations), 200

# New API to Load Movie Data from JSON File
@main_routes.route('/load-movies', methods=['GET'])
def load_movies():
    try:
        # Load movies from the movies_data.json file
        with open('/Users/shekharsuman/MyMovieReco/data/movies_data.json', 'r') as f:
            movies = json.load(f)
        
        # Insert each movie into Redis
        for movie in movies:
            insert_movie_into_redis(movie)       
        return jsonify({'message': f'{len(movies)} movies inserted into Redis successfully!'}), 200
    
    except FileNotFoundError:
        return jsonify({'message': 'Movies data file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
