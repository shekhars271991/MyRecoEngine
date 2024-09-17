from models.Movie import Movie
from services.user_profiles import get_user_profile, update_user_profile
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to generate movie recommendations based on user profile
def get_recommendations(user):
    profile_vector = get_user_profile(user)
    all_movies = Movie.get_all_movies()
    
    # Prepare movie feature matrix
    movie_vectors = [movie.get_feature_vector() for movie in all_movies]
    
    # Calculate similarity scores
    similarity_scores = cosine_similarity([profile_vector], movie_vectors)[0]
    
    # Sort and return the most similar movies
    sorted_indices = np.argsort(-similarity_scores)
    recommended_movies = [all_movies[i].serialize() for i in sorted_indices[:5]]
    return recommended_movies
