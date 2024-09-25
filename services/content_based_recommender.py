from models.Movie import Movie
from services.user_profiles import get_user_profile
from services.redisvl_service import search_movies_by_vector_with_filters
from services.redis_service import getJson
import numpy as np
from config import NUM_RECO, SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD

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
        movie_details = getJson(movie_id)
        
        if movie_details:
            # Exclude embeddings
            if 'embeddings' in movie_details:
                movie_details.pop('embeddings')
            
            # Add the movie to the list if vector distance <= SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD
            vector_distance = float(result['vector_distance'])  # Convert to float for comparison
            if vector_distance <= SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD:
                movie_details['vector_distance'] = vector_distance
                recommended_movies.append(movie_details)
    
    # Sort by vector distance and limit to the 5 movies with the least distance
    recommended_movies = sorted(recommended_movies, key=lambda x: x['vector_distance'])[:5]

    return recommended_movies, 200
