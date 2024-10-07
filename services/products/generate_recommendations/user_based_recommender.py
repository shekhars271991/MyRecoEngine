# product_user_based_recommender.py

from services.db.redisvl_service import search_similar_product_users
from services.db.redis_service import getJson, get_user_product_profile
from config.config import SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD

def get_similar_users_product_profile(user):
    profile = get_user_product_profile(user)
    if profile is None:
        return {
            "error": "User profile not found."
        }, 404
    profile_vector = profile.get('feature_weights', [])
    results = search_similar_product_users(profile_vector, index_name='product_user_profiles')

    # Filter the results: Exclude the current user and only include users with a vector distance < threshold
    filtered_results = []
    for result_user in results:
        # Ensure we're not comparing the user with themselves
        if result_user["id"] != user.product_profile_key:
            # Check if the vector distance is less than the threshold
            vector_distance = float(result_user.get('vector_distance', 1.0))  # Default to 1.0 if not found
            if vector_distance < SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD:
                # Fetch additional user details, such as ratings
                filtered_user_id = result_user["id"]
                user_details = getJson(filtered_user_id)
                result_user["ratings"] = user_details.get('ratings', {})  # Default to empty dict if not found
                filtered_results.append(result_user)

    # Return the filtered results
    return filtered_results, 200

def get_rated_products_of_related_users(user):
    # Unpack the result and status code from get_similar_users_product_profile
    similar_users, status_code = get_similar_users_product_profile(user)

    # Check for errors
    if status_code == 404:
        return {
            "error": "User profile not found."
        }, 404

    # Dictionary to store products and their ratings
    products_with_ratings = {}

    # Iterate through the similar users' results
    for result_user in similar_users:
        # Ensure we're not comparing the user with themselves
        if result_user["id"] != user.product_profile_key:
            # Fetch user details and ratings
            filtered_user_id = result_user["id"]
            user_details = getJson(filtered_user_id)

            # Add all products from the user's ratings to the dictionary
            rated_products = user_details.get('ratings', {})
            for product_id, rating in rated_products.items():
                # Handle duplicate ratings by taking the higher rating
                if product_id in products_with_ratings:
                    products_with_ratings[product_id] = max(products_with_ratings[product_id], rating)
                else:
                    products_with_ratings[product_id] = rating

    # Convert the dictionary to a list of dictionaries for the response
    products_list = [{"product_id": product_id, "rating": rating} for product_id, rating in products_with_ratings.items()]

    return products_list, 200
