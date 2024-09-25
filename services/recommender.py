from services.user_based_recommender import get_rated_movies_of_related_users
from services.content_based_recommender import get_recommendations

def get_combined_recommendations(user, genres=None, min_year=None, max_year=None):
    combined_Reco = {}

    user_reco, user_status_code = get_rated_movies_of_related_users(user)
    if user_status_code == 404:
        return {"error": "User profile not found"}, 404
    
    # Fetch content-based recommendations
    content_reco, content_status_code = get_recommendations(user, genres, min_year, max_year)
    if content_status_code == 404:
        return {"error": "Recommendations not found"}, 404
    
    sorted_content_reco = sorted(content_reco, key=lambda x: x.get('vector_distance', 1.0))

 # Combine both recommendations in the result dictionary
    combined_Reco['user_reco'] = user_reco
    combined_Reco['content_reco'] = sorted_content_reco

    # Return the combined recommendations with a success status
    return combined_Reco, 200
