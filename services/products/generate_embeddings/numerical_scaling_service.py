# numerical_scaling_service.py

import numpy as np
from sklearn.preprocessing import MinMaxScaler

import numpy as np
import json

# Load predefined scaling parameters from the config file
with open('config/numerical_scaling_config.json', 'r') as f:
    scaling_config = json.load(f)

# Initialize scaler
scaler = MinMaxScaler()

def scale_numerical_features(product):
    # Extract the predefined min and max values from the config
    price_min = scaling_config['price']['min']
    price_max = scaling_config['price']['max']
    release_year_min = scaling_config['release_year']['min']
    release_year_max = scaling_config['release_year']['max']
    rating_min = scaling_config['rating']['min']
    rating_max = scaling_config['rating']['max']
    reviews_count_min = scaling_config['reviews_count']['min']
    reviews_count_max = scaling_config['reviews_count']['max']
    stock_min = scaling_config['stock']['min']
    stock_max = scaling_config['stock']['max']

    # Parse the product's numerical features
    price = parse_price(product.get('price', '$0'))
    release_year = product.get('release_year', release_year_min)
    rating = product.get('rating', rating_min)
    reviews_count = product.get('reviews_count', reviews_count_min)
    stock = product.get('stock', stock_min)

    # Manually scale each feature using min-max scaling
    def min_max_scale(value, min_value, max_value):
        # Handle division by zero if min and max are equal
        if max_value - min_value == 0:
            return 0.0
        # Optionally clip the value to the min and max range
        value = max(min_value, min(value, max_value))
        return (value - min_value) / (max_value - min_value)

    scaled_price = min_max_scale(price, price_min, price_max)
    scaled_release_year = min_max_scale(release_year, release_year_min, release_year_max)
    scaled_rating = min_max_scale(rating, rating_min, rating_max)
    scaled_reviews_count = min_max_scale(reviews_count, reviews_count_min, reviews_count_max)
    scaled_stock = min_max_scale(stock, stock_min, stock_max)

    numerical_vector = np.array([scaled_price, scaled_release_year, scaled_rating, scaled_reviews_count, scaled_stock])
    return numerical_vector

def parse_price(price_str):
    price_str = price_str.replace('$', '').replace(',', '').strip()
    try:
        return float(price_str)
    except ValueError:
        return 0.0
