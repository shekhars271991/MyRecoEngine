from models.Movie import Movie
from services.user_profiles import get_user_profile, update_user_profile
from services.redisvl_service import search_movies_by_vector 
import numpy as np
from config import NUM_RECO

# Function to generate movie recommendations based on user profile
def get_recommendations(user):
    # Get the user's profile vector
    profile_vector = get_user_profile(user)
    
    # Perform a vector search on the Redis index
    results = search_movies_by_vector(profile_vector, num_results=NUM_RECO)
    
    # Extract movie data from the search results
    recommended_movies = []
    for result in results:
        # Each 'result' is an object with the movie data and metadata
        movie_data = {
            'id': result['id'],
            'release_year': result['release_year'],
            'genres': result['genres'],
            'vector_distance': result['vector_distance']
        }
        recommended_movies.append(movie_data)
    
    return recommended_movies
