from flask import Flask, request, jsonify
from services.auth import authenticate_user, login_required
from services.recommender import get_recommendations
from models import Movie, User
from redis_client import redis_client

app = Flask(__name__)

# User Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    token = authenticate_user(username, password)
    if token:
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Get Movie List Route (with descriptions and cast)
@app.route('/movies', methods=['GET'])
@login_required
def get_movies(user):
    movies = Movie.get_all_movies()
    return jsonify([movie.serialize() for movie in movies]), 200

# User Action: Watched/Not Watched, Rating Route
@app.route('/movies/action', methods=['POST'])
@login_required
def movie_action(user):
    movie_id = request.json.get('movie_id')
    watched = request.json.get('watched')
    rating = request.json.get('rating', None)
    
    user.update_movie_status(movie_id, watched, rating)
    return jsonify({'message': 'Action updated successfully'}), 200

# Get Recommendations Route
@app.route('/movies/recommendations', methods=['GET'])
@login_required
def get_movie_recommendations(user):
    recommendations = get_recommendations(user)
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True)
