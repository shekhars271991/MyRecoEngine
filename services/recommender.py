from services.user_based_recommender import get_rated_movies_of_related_users
from services.content_based_recommender import get_recommendations
from services.redis_service import getJson  # Import the getJson function
from config import CONTENT_BASED_RECO_COUNT


def get_combined_recommendations(user, genres=None, min_year=None, max_year=None):
    combined_Reco = {}

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

    # Fetch and append movie details for user-based recommendations
    user_reco_with_details = []
    for reco in user_reco:
        movie_id = reco['movie_id']
        movie_details = getJson(movie_id)  # Fetch movie details from Redis
        if movie_details:
            # Remove embeddings if present
            movie_details.pop('embeddings', None)
            
            # Append movie details and rating
            reco_with_details = {
                "movie_id": movie_id,
                "rating": reco['rating'],
                "details": movie_details  # Append movie details here
            }
            user_reco_with_details.append(reco_with_details)

    # Fetch and append movie details for content-based recommendations
    content_reco_with_details = []
    for reco in sorted_content_reco:
        movie_id = reco['id']
        movie_details = getJson(movie_id)  # Fetch movie details from Redis
        if movie_details:
            # Remove embeddings if present
            movie_details.pop('embeddings', None)
            
            # Append movie details and vector distance
            reco_with_details = {
                "movie_id": movie_id,
                "vector_distance": reco['vector_distance'],
                "details": movie_details  # Append movie details here
            }
            content_reco_with_details.append(reco_with_details)

    # Combine both recommendations in the result dictionary
    combined_Reco['user_reco'] = user_reco_with_details
    combined_Reco['content_reco'] = content_reco_with_details

    # Return the combined recommendations with a success status
    return combined_Reco, 200
