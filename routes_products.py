from flask import Blueprint, request, jsonify
from services.products.load_products import load_product_data
import json

products_routes = Blueprint('products_routes', __name__)

@products_routes.route('/products/load-products', methods=['GET'])
def load_products():
    try:
        with open('data/cleaned_products_data.json', 'r') as f:
            products = json.load(f)
        for product in products:
            load_product_data(product) 
        return jsonify({'message': f'{len(products)} products inserted into Redis successfully!'}), 200
    except FileNotFoundError:
        return jsonify({'message': 'Products data file not found.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
