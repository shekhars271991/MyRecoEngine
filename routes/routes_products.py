# routes_products.py

from flask import Blueprint, request, jsonify
from services.auth import login_required
from models.Product import Product  # Assuming you have a Product model
from models.User import User
import json
import re
from services.db.redis_service import exists, getJson
from config.config import PRODUCTS_DATA_FILEPATH

from services.products.load_products import load_all_products
from services.db.redis_service import get_all_products


products_routes = Blueprint('products_routes', __name__, url_prefix='/product')

def get_combined_product_recommendations():
    return

@products_routes.route('/', methods=['GET'])
@login_required
def get_products(user):
    # Get page and page_size from query parameters (with defaults)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # Get paginated products and total count, with the status filter
    products, total_products = get_all_products(page, page_size)

    # Build the response with pagination info
    response = {
        'products': products,
        'page': page,
        'page_size': page_size,
        'total_products': total_products,
        'total_pages': (total_products + page_size - 1) // page_size
    }

    return jsonify(response), 200


@products_routes.route('/rate', methods=['POST'])
@login_required
def product_action(user: User):
    product_id = request.json.get('product_id')
    rating = request.json.get('rating', None)
   
    product_exists = exists(product_id)

    if not product_exists:
        return jsonify({'message': 'Product not found.'}), 404

    try:
        user.rate_product(product_id, rating)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    return jsonify({'message': 'Action updated successfully'}), 200


@products_routes.route('/recommendations', methods=['GET'])
@login_required
def get_product_recommendations(user):
    # Extract query parameters
    categories = request.args.get('categories')  # Could be a comma-separated string
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    # Process categories to a list if provided
    if categories:
        categories = [category.strip() for category in categories.split(',')]
    else:
        categories = None

    # Convert min_price and max_price to floats if provided
    try:
        min_price = float(min_price) if min_price else None
    except ValueError:
        return jsonify({'error': 'Invalid min_price parameter'}), 400

    try:
        max_price = float(max_price) if max_price else None
    except ValueError:
        return jsonify({'error': 'Invalid max_price parameter'}), 400

    # Get recommendations with filters
    recommendations, status_code = get_combined_product_recommendations(
        user,
        categories=categories,
        min_price=min_price,
        max_price=max_price
    )
    if status_code == 404:
        return jsonify({"error": "User profile not found."}), 404

    return jsonify(recommendations), 200

@products_routes.route('/load', methods=['GET'])
def load_products():
    try:
        # Load products from the JSON file
        with open(PRODUCTS_DATA_FILEPATH, 'r') as f:
            products = json.load(f)

        load_all_products(products)

        return jsonify({'message': f'{len(products)} products inserted into Redis successfully!'}), 200

    except FileNotFoundError:
        return jsonify({'message': 'Products data file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500