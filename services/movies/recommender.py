from services.movies.user_based_recommender import get_rated_movies_of_related_users
from services.movies.content_based_recommender import get_recommendations
from services.db.redis_service import getJson  # Import the getJson function
from config.config import CONTENT_BASED_RECO_COUNT


def get_combined_recommendations(user, genres=None, min_year=None, max_year=None):
    combined_Reco = []

    # Fetch user-based recommendations
    user_reco, user_status_code = get_rated_movies_of_related_users(user)
    if user_status_code == 404:
        return {"error": "User profile not found"}, 404
    
    # Fetch content-based recommendations
    content_reco, content_status_code = get_recommendations(user, genres, min_year, max_year)
    if content_status_code == 404:
        return {"error": "Recommendations not found"}, 404
    
    # Sort content-based recommendations by vector distance and limit to the top N
    sorted_content_reco = sorted(content_reco, key=lambda x: x.get('vector_distance', 1.0))[:CONTENT_BASED_RECO_COUNT]

    # Create a dictionary to store combined movie recommendations with type
    combined_movies = {}

    # Process user-based recommendations
    for reco in user_reco:
        movie_id = reco['movie_id']
        movie_details = getJson(movie_id)  # Fetch movie details from Redis
        if movie_details:
            # Remove embeddings if present
            movie_details.pop('embeddings', None)
            
            # If the movie is already in combined_movies, it means it's in both lists
            if movie_id in combined_movies:
                combined_movies[movie_id]['type'].append('user')
                combined_movies[movie_id]['rating'] = reco['rating']  # Update rating
            else:
                # Add the movie to combined_movies with user recommendation
                combined_movies[movie_id] = {
                    "movie_id": movie_id,
                    "rating": reco['rating'],
                    "details": movie_details,
                    "type": ['user'],  # Start with user type
                    "vector_distance": None  # Set to None initially
                }

    # Process content-based recommendations
    for reco in sorted_content_reco:
        movie_id = reco['id']
        movie_details = getJson(movie_id)  # Fetch movie details from Redis
        if movie_details:
            # Remove embeddings if present
            movie_details.pop('embeddings', None)
            
            # If the movie is already in combined_movies, it's in both lists
            if movie_id in combined_movies:
                combined_movies[movie_id]['type'].append('content')
                combined_movies[movie_id]['vector_distance'] = reco['vector_distance']  # Update vector distance
            else:
                # Add the movie to combined_movies with content recommendation
                combined_movies[movie_id] = {
                    "movie_id": movie_id,
                    "rating": None,  # Set to None as it's from content reco
                    "details": movie_details,
                    "type": ['content'],  # Start with content type
                    "vector_distance": reco['vector_distance']
                }

    # Convert the dictionary to a list and rank the movies
    combined_list = []
    for movie in combined_movies.values():
        combined_list.append(movie)

    # Rank the movies:
    # - Higher rank for movies that appear in both `user` and `content`
    # - Higher rank for higher ratings
    # - Lower vector distance gets a higher rank
    combined_list = sorted(combined_list, key=lambda x: (
        'both' in x['type'],  # Prioritize movies in both lists
        x['rating'] or 0,  # Higher rating gets priority
        -x['vector_distance'] if x['vector_distance'] is not None else 1.0  # Lower vector distance gets priority
    ), reverse=True)

    # Add the rank to each movie
    for rank, movie in enumerate(combined_list, start=1):
        movie['rank'] = rank

    # Return the combined recommendations with a success status
    return combined_list, 200
