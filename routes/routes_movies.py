from flask import Blueprint, request, jsonify
from services.auth import authenticate_user, register_user, login_required
from services.movies.recommender import get_combined_recommendations
from services.movies.user_based_recommender import get_similar_users_profile
from models.Movie import Movie
from models.User import User
import json
import re
from services.movies.load_movies import load_movie_data 
from services.db.redis_service import exists, getJson



movie_routes = Blueprint('movie_routes', __name__, url_prefix="/movies")

# # User Registration Route
# @main_routes.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     name = data.get('name')
#     username = data.get('username')
#     password = data.get('password')
    
#     # Input validation
#     if not name or not username or not password:
#         return jsonify({'message': 'All fields are required'}), 400

#     # Validate username (e.g., alphanumeric, min length)
#     if not re.match(r'^\w{3,}$', username):
#         return jsonify({'message': 'Invalid username format'}), 400

#     # Validate password length
#     if len(password) < 4:
#         return jsonify({'message': 'Password must be at least 6 characters long'}), 400

#     if register_user(name, username, password):
#         return jsonify({'message': 'User registered successfully'}), 201
#     else:
#         return jsonify({'message': 'User already exists or invalid data'}), 400

# User Login Route
# @main_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     token = authenticate_user(username, password)
#     if token:
#         return jsonify({'access_token': token}), 200
#     return jsonify({'message': 'Invalid credentials'}), 401

# Get Movie List Route (with descriptions and cast)
@movie_routes.route('/', methods=['GET'])
@login_required
def get_movies(user):
    # Get page and page_size from query parameters (with defaults)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    # Get the status query param (could be "seen", "not_seen", or "new")
    status = request.args.get('status', None)

    # Get paginated movies and total count, with the status filter
    movies, total_movies = Movie.get_all_movies(user, page, page_size, status)

    # Build the response with pagination info
    response = {
        'movies': movies,
        'page': page,
        'page_size': page_size,
        'total_movies': total_movies,
        'total_pages': (total_movies + page_size - 1) // page_size  # Calculate total pages
    }

    return jsonify(response), 200

# User Action: Watched/Not Watched, Rating Route
@movie_routes.route('/action', methods=['POST'])
@login_required
def movie_action(user: User):
    movie_id = request.json.get('movie_id')
    watched = request.json.get('watched')
    rating = request.json.get('rating', None)
    # user_instance = User(username=user)
   
    movie_exists = exists(movie_id)

    if not movie_exists:
        return jsonify({'message': 'Movie not found.'}), 404

    try:
        user.update_movie_status(movie_id, watched, rating)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    # user.update_movie_status(movie_key, watched, rating)
    return jsonify({'message': 'Action updated successfully'}), 200


@movie_routes.route('/recommendations', methods=['GET'])
@login_required
def get_movie_recommendations(user):
    # Extract query parameters
    genres = request.args.get('genres')  # Could be a comma-separated string
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')

    # Process genres to a list if provided
    if genres:
        genres = [genre.strip() for genre in genres.split(',')]
    else:
        genres = None

    # Convert min_year and max_year to integers if provided
    try:
        min_year = int(min_year) if min_year else None
    except ValueError:
        return jsonify({'error': 'Invalid min_year parameter'}), 400

    try:
        max_year = int(max_year) if max_year else None
    except ValueError:
        return jsonify({'error': 'Invalid max_year parameter'}), 400

    # Get recommendations with filters
    recommendations, status_code = get_combined_recommendations(
        user,
        genres=genres,
        min_year=min_year,
        max_year=max_year
    )
    if status_code == 404:
        return jsonify({"error": "User profile not found."}), 404
   
    return jsonify(recommendations), 200

# New API to Load Movie Data from JSON File
@movie_routes.route('/load-movies', methods=['GET'])
def load_movies():
    try:
        # Load movies from the movies_data.json file
        with open('data/cleaned_movies_data.json', 'r') as f:
            movies = json.load(f)
        
        # Insert each movie into Redis
        for movie in movies:
            load_movie_data(movie) 
        return jsonify({'message': f'{len(movies)} movies inserted into Redis successfully!'}), 200
    
    except FileNotFoundError:
        return jsonify({'message': 'Movies data file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# User Profile Route
@movie_routes.route('/profile', methods=['GET'])
@login_required
def get_user_profile(user: User):
    try:
        # Fetch user profile details
        userprofile_key = "profile:" + user.username
        profile = getJson(userprofile_key)
        if 'feature_weights' in profile:
            profile.pop('feature_weights')
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Similar Users Route
@movie_routes.route('/similar-users', methods=['GET'])
@login_required
def similar_users(user):
    try:
        # Get recommendations with filters
        similarUsers, status_code = get_similar_users_profile(
            user
        )
        if status_code == 404:
            return jsonify({"error": "User profile not found."}), 404
        return jsonify(similarUsers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500