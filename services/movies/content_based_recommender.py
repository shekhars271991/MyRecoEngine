from models.Movie import Movie
from services.db.redis_service import get_user_movie_profile
from services.db.redisvl_service import search_movies_by_vector_with_filters
import numpy as np
from config.config import NUM_RECO, SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD

# Function to generate movie recommendations based on user profile
def get_recommendations(user, genres=None, min_year=None, max_year=None):
    # Get the user's profile vector
    profile = get_user_movie_profile(user)
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
    
    # Extract movie IDs from the search results, filtering out watched movies and those with high vector distance
    recommended_movies = []
    for result in results:
        movie_id = result['id']
        
        # Skip the movie if the user has already watched it
        if movie_id in watched_movies:
            continue
        
        # Filter based on vector distance
        vector_distance = float(result['vector_distance'])  # Convert to float for comparison
        if vector_distance <= SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD:
            recommended_movies.append({
                'id': movie_id,
                'vector_distance': vector_distance
            })  # Store the movie ID and its vector distance
    
    # Sort by vector distance and limit to the top movies with the least distance
    # recommended_movies = sorted(recommended_movies, key=lambda x: x['vector_distance'])[:CONTENT_BASED_RECO_COUNT]

    # Return only the movie IDs
    return recommended_movies, 200
