from flask import Blueprint, request, jsonify
from services.auth import login_required
from services.movies.recommender import get_combined_recommendations
from services.movies.user_based_recommender import get_similar_users_profile
from models.Movie import Movie
from models.User import User
from services.movies.load_movies import load_movie_data
from services.db.redis_service import exists, getJson
import json

movies_routes = Blueprint('movies_routes', __name__)

@movies_routes.route('/movies', methods=['GET'])
@login_required
def get_movies(user):
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    status = request.args.get('status', None)
    movies, total_movies = Movie.get_all_movies(user, page, page_size, status)
    response = {
        'movies': movies,
        'page': page,
        'page_size': page_size,
        'total_movies': total_movies,
        'total_pages': (total_movies + page_size - 1) // page_size
    }
    return jsonify(response), 200

@movies_routes.route('/movies/action', methods=['POST'])
@login_required
def movie_action(user: User):
    movie_id = request.json.get('movie_id')
    watched = request.json.get('watched')
    rating = request.json.get('rating', None)
    
    movie_exists = exists(movie_id)
    if not movie_exists:
        return jsonify({'message': 'Movie not found.'}), 404

    try:
        user.update_movie_status(movie_id, watched, rating)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'message': 'Action updated successfully'}), 200

@movies_routes.route('/movies/recommendations', methods=['GET'])
@login_required
def get_movie_recommendations(user):
    genres = request.args.get('genres')
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')

    if genres:
        genres = [genre.strip() for genre in genres.split(',')]
    else:
        genres = None

    try:
        min_year = int(min_year) if min_year else None
    except ValueError:
        return jsonify({'error': 'Invalid min_year parameter'}), 400

    try:
        max_year = int(max_year) if max_year else None
    except ValueError:
        return jsonify({'error': 'Invalid max_year parameter'}), 400

    recommendations, status_code = get_combined_recommendations(
        user,
        genres=genres,
        min_year=min_year,
        max_year=max_year
    )
    if status_code == 404:
        return jsonify({"error": "User profile not found."}), 404
   
    return jsonify(recommendations), 200

@movies_routes.route('/movies/load-movies', methods=['GET'])
def load_movies():
    try:
        with open('data/cleaned_movies_data.json', 'r') as f:
            movies = json.load(f)
        for movie in movies:
            load_movie_data(movie) 
        return jsonify({'message': f'{len(movies)} movies inserted into Redis successfully!'}), 200
    except FileNotFoundError:
        return jsonify({'message': 'Movies data file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@movies_routes.route('/movies/similar-users', methods=['GET'])
@login_required
def similar_users(user):
    try:
        similarUsers, status_code = get_similar_users_profile(user)
        if status_code == 404:
            return jsonify({"error": "User profile not found."}), 404
        return jsonify(similarUsers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
