from models.Movie import Movie
from services.user_profiles import get_user_profile
from services.redisvl_service import search_movies_by_vector_with_filters
import numpy as np
from config import NUM_RECO
import json

# Function to generate movie recommendations based on user profile
def get_recommendations(user, genres=None, min_year=None, max_year=None):
    # Get the user's profile vector
    profile = get_user_profile(user)
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
        
        genres_field = result.get('genres')
        if isinstance(genres_field, str):
            try:
                # Parse the JSON string into a Python list
                genres_list = json.loads(genres_field)
            except json.JSONDecodeError:
                # If parsing fails, wrap the string in a list
                genres_list = [genres_field]
        elif isinstance(genres_field, list):
            genres_list = genres_field
        else:
            genres_list = []

        # Add the movie to the list of recommendations
        movie_data = {
            'id': movie_id,
            'genres': genres_list,
            'release_year': result['release_year'],
            'vector_distance': result['vector_distance']
        }
        recommended_movies.append(movie_data)
    
    return recommended_movies
