from services.db.redisvl_service import search_similar_users
from services.db.redis_service import getJson, get_user_profile
from config.config import SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD

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
                result_user["ratings"] = user_details.get('ratings', {})  # Default to an empty dictionary if not found
                filtered_results.append(result_user)

    # Return the filtered results
    return filtered_results, 200


def get_rated_movies_of_related_users(user):
    # Unpack the result and status code from get_similar_users_profile
    similar_users, status_code = get_similar_users_profile(user)

    # Check for errors
    if status_code == 404:
        return {
            "error": "User profile not found."
        }, 404

    # Dictionary to store movies and their ratings
    movies_with_ratings = {}

    # Iterate through the similar users' results
    for result_user in similar_users:
        # Ensure we're not comparing the user with themselves
        if result_user["id"] != user.profile_key:
            # Check if the vector distance is less than SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD
            vector_distance = float(result_user.get('vector_distance', 1.0))  # Default to 1.0 if not found
            if vector_distance < SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD:
                # Fetch additional user details, such as ratings, from Redis or DB
                filtered_user_id = result_user["id"]
                user_details = getJson(filtered_user_id)
                
                # Add all movies from the user's ratings to the dictionary
                rated_movies = user_details.get('ratings', {})
                for movie_id, rating in rated_movies.items():
                    # If the movie is already in the dictionary, you may handle duplicate ratings (e.g., take the max rating)
                    if movie_id in movies_with_ratings:
                        # If already present, take the higher rating
                        movies_with_ratings[movie_id] = max(movies_with_ratings[movie_id], rating)
                    else:
                        # Otherwise, just add the movie and its rating
                        movies_with_ratings[movie_id] = rating

    # Convert the dictionary to a list of dictionaries for the response
    movies_list = [{"movie_id": movie_id, "rating": rating} for movie_id, rating in movies_with_ratings.items()]
    
    return movies_list, 200
