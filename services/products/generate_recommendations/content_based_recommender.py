# product_content_based_recommender.py

from models.Product import Product
from services.db.redis_service import get_user_product_profile
from services.db.redisvl_service import search_products_by_vector
from config.config import NUM_RECO, SIMILAR_PRODUCT_VECTOR_DISTANCE_THRESHOLD

def get_product_recommendations(user, categories=None, min_price=None, max_price=None):
    # Get the user's product profile vector
    profile = get_user_product_profile(user)
    if profile is None:
        return {
            "error": "User profile not found."
        }, 404
    profile_vector = profile.get('feature_weights', [])

    # Get the list of products the user has already rated
    rated_products = set(profile.get('rated_products', []))

    # Perform a vector search on the Redis index with optional filters
    results = search_products_by_vector(
        query_vector=profile_vector,
        categories=categories,
        min_price=min_price,
        max_price=max_price,
        num_results=NUM_RECO
    )

    # Extract product IDs from the search results, filtering out rated products and those with high vector distance
    recommended_products = []
    for result in results:
        product_id = result['id']

        # Skip the product if the user has already rated it
        # if product_id in rated_products:
        #     continue

        # Filter based on vector distance
        vector_distance = float(result['vector_distance'])  # Convert to float for comparison
        if vector_distance <= SIMILAR_PRODUCT_VECTOR_DISTANCE_THRESHOLD:
            recommended_products.append({
                'id': product_id,
                'vector_distance': vector_distance
            })  # Store the product ID and its vector distance

    # Return the recommended products
    return recommended_products, 200
