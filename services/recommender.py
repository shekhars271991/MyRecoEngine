from models.Movie import Movie
from services.user_profiles import get_user_profile
from services.redisvl_service import search_movies_by_vector_with_filters
from services.redis_service import redis_client  # Assuming this is the service for interacting with Redis
import numpy as np
from config import NUM_RECO

# Function to generate movie recommendations based on user profile
def get_recommendations(user, genres=None, min_year=None, max_year=None):
    # Get the user's profile vector
    profile = get_user_profile(user)
    if profile is None:
        return {
            "error": "User profile not found."
        }, 404
    profile_vector = profile.get('feature_weights', [])
    
    # Get the list of movies the user has already watched
    watched_movies = set(profile.get('watched', []))

    # Perform a vector search on the Redis index with optional filters
    results = search_movies_by_vector_with_filters(
        query_vector=profile_vector,
        genres=genres,
        min_year=min_year,
        max_year=max_year,
        num_results=NUM_RECO
    )
    
    # Extract movie data from the search results, filtering out watched movies
    recommended_movies = []
    for result in results:
        movie_id = result['id']
        
        # Skip the movie if the user has already watched it
        if movie_id in watched_movies:
            continue
        
        # Fetch full movie details from Redis
        movie_details = redis_client.json().get(movie_id)
        
        if movie_details:
            # Exclude embeddings
            if 'embeddings' in movie_details:
                movie_details.pop('embeddings')
            
            # Add the movie to the list of recommendations
            movie_details['vector_distance'] = result['vector_distance']  # Add vector distance from the result
            recommended_movies.append(movie_details)
    
    return recommended_movies, 200

