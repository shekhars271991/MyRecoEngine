from services.redisvl_service import search_similar_users
from services.user_profiles import get_user_profile
from services.redis_service import getJson

def get_similar_users_profile(user):
    profile = get_user_profile(user)
    if profile is None:
        return {
            "error": "User profile not found."
        }, 404
    profile_vector = profile.get('feature_weights', [])
    results = search_similar_users(profile_vector)
    filtered_results = [result_user for result_user in results if result_user["id"] != user.profile_key]
    for filtered_user in filtered_results:
            filtered_user_id = filtered_user["id"]
            user_details = getJson(filtered_user_id)  # Fetch watched list from Redis or DB
            filtered_user["ratings"] = user_details['ratings']
        
    return filtered_results, 200
