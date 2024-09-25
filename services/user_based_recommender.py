from services.redisvl_service import search_similar_users
from services.user_profiles import get_user_profile
from services.redis_service import getJson
from config import SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD

def get_similar_users_profile(user):
    profile = get_user_profile(user)
    if profile is None:
        return {
            "error": "User profile not found."
        }, 404
    profile_vector = profile.get('feature_weights', [])
    results = search_similar_users(profile_vector)
    
    # Filter the results: Exclude the current user and only include users with a vector distance < SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD
    filtered_results = []
    for result_user in results:
        # Ensure we're not comparing the user with themselves
        if result_user["id"] != user.profile_key:
            # Check if the vector distance is less than SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD
            vector_distance = float(result_user.get('vector_distance', 1.0))  # Default to 1.0 if not found
            if vector_distance < SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD:
                # Fetch additional user details, such as ratings, from Redis or DB
                filtered_user_id = result_user["id"]
                user_details = getJson(filtered_user_id)
                result_user["ratings"] = user_details.get('ratings', [])  # Default to an empty list if not found
                filtered_results.append(result_user)

    # Return the filtered results
    return filtered_results, 200