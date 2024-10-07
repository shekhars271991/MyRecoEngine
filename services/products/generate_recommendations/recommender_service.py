# product_recommender_service.py

from services.products.generate_recommendations.user_based_recommender import get_rated_products_of_related_users
from services.products.generate_recommendations.content_based_recommender import get_product_recommendations
from services.db.redis_service import getJson 
from config.config import CONTENT_BASED_RECO_COUNT

def get_combined_product_recommendations(user, categories=None, min_price=None, max_price=None):
    combined_reco = []

    # Fetch user-based recommendations
    user_reco, user_status_code = get_rated_products_of_related_users(user)
    if user_status_code == 404:
        return {"error": "User profile not found"}, 404

    # Fetch content-based recommendations
    content_reco, content_status_code = get_product_recommendations(user, categories, min_price, max_price)
    if content_status_code == 404:
        return {"error": "Recommendations not found"}, 404

    # Sort content-based recommendations by vector distance and limit to the top N

    # Create a dictionary to store combined product recommendations with type
    combined_products = {}

    # Process user-based recommendations
    for reco in user_reco:
        product_id = reco['product_id']
        product_details = getJson(f"{product_id}")  # Fetch product details from Redis
        if product_details:
            # Remove vector if present
            product_details.pop('embeddings', None)

            # If the product is already in combined_products, it means it's in both lists
            if product_id in combined_products:
                combined_products[product_id]['type'].append('user')
                combined_products[product_id]['rating'] = reco['rating']  # Update rating
            else:
                # Add the product to combined_products with user recommendation
                combined_products[product_id] = {
                    "product_id": product_id,
                    "rating": reco['rating'],
                    "details": product_details,
                    "type": ['user'],  # Start with user type
                    "vector_distance": None  # Set to None initially
                }

    # Process content-based recommendations
    for reco in content_reco:
        product_id = reco['id']
        product_details = getJson(f"{product_id}")  # Fetch product details from Redis
        if product_details:
            # Remove vector if present
            product_details.pop('embeddings', None)

            # If the product is already in combined_products, it's in both lists
            if product_id in combined_products:
                combined_products[product_id]['type'].append('content')
                combined_products[product_id]['vector_distance'] = reco['vector_distance']  # Update vector distance
            else:
                # Add the product to combined_products with content recommendation
                combined_products[product_id] = {
                    "product_id": product_id,
                    "rating": None,  # Set to None as it's from content reco
                    "details": product_details,
                    "type": ['content'],  # Start with content type
                    "vector_distance": reco['vector_distance']
                }

    # Convert the dictionary to a list and rank the products
    combined_list = list(combined_products.values())

    # Rank the products:
    # - Higher rank for products that appear in both user and content
    # - Higher rank for higher ratings
    # - Lower vector distance gets a higher rank
    combined_list = sorted(combined_list, key=lambda x: (
        'both' in x['type'],  # Prioritize products in both lists
        x['rating'] or 0,  # Higher rating gets priority
        -x['vector_distance'] if x['vector_distance'] is not None else 1.0  # Lower vector distance gets priority
    ), reverse=True)

    # Add the rank to each product
    for rank, product in enumerate(combined_list, start=1):
        product['rank'] = rank

    # Return the combined recommendations with a success status
    return combined_list, 200
