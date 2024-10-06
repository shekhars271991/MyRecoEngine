# categorical_encoding_service.py

import numpy as np
from sklearn.preprocessing import OneHotEncoder
import json

# Load predefined categories from the config file
with open('config/categories_config.json', 'r') as f:
    config = json.load(f)

# Extract categories from the config
categories_list = config['categories']
features_list = config['features']
colors_list = config['colors']
manufacturers_list = config['manufacturers']
countries_list = config['countries']

# Initialize OneHotEncoders with predefined categories
category_encoder = OneHotEncoder(categories=[categories_list], handle_unknown='ignore', sparse_output=False)
feature_encoder = OneHotEncoder(categories=[features_list], handle_unknown='ignore', sparse_output=False)
color_encoder = OneHotEncoder(categories=[colors_list], handle_unknown='ignore', sparse_output=False)
manufacturer_encoder = OneHotEncoder(categories=[manufacturers_list], handle_unknown='ignore', sparse_output=False)
country_encoder = OneHotEncoder(categories=[countries_list], handle_unknown='ignore', sparse_output=False)

# Fit the encoders (required even when categories are predefined)
def fit_encoders():
    # For OneHotEncoder, fit on any data that contains all categories
    category_encoder.fit(np.array(categories_list).reshape(-1, 1))
    feature_encoder.fit(np.array(features_list).reshape(-1, 1))
    color_encoder.fit(np.array(colors_list).reshape(-1, 1))
    manufacturer_encoder.fit(np.array(manufacturers_list).reshape(-1, 1))
    country_encoder.fit(np.array(countries_list).reshape(-1, 1))

# Call fit_encoders() to fit all encoders
fit_encoders()

# Store vector sizes
CATEGORY_VECTOR_SIZE = len(categories_list)
FEATURE_VECTOR_SIZE = len(features_list)
COLOR_VECTOR_SIZE = len(colors_list)
MANUFACTURER_VECTOR_SIZE = len(manufacturers_list)
COUNTRY_VECTOR_SIZE = len(countries_list)

def encode_categories(categories):
    if categories:
        encoded = category_encoder.transform(np.array(categories).reshape(-1, 1))
        vector = encoded.sum(axis=0)
    else:
        vector = np.zeros(CATEGORY_VECTOR_SIZE)
    return vector

def encode_features(features):
    if features:
        encoded = feature_encoder.transform(np.array(features).reshape(-1, 1))
        vector = encoded.sum(axis=0)
    else:
        vector = np.zeros(FEATURE_VECTOR_SIZE)
    return vector

def encode_colors(colors):
    if colors:
        encoded = color_encoder.transform(np.array(colors).reshape(-1, 1))
        vector = encoded.sum(axis=0)
    else:
        vector = np.zeros(COLOR_VECTOR_SIZE)
    return vector

def encode_manufacturer(manufacturer):
    if manufacturer:
        encoded = manufacturer_encoder.transform([[manufacturer]])
        vector = encoded.flatten()
    else:
        vector = np.zeros(MANUFACTURER_VECTOR_SIZE)
    return vector

def encode_country(country):
    if country:
        encoded = country_encoder.transform([[country]])
        vector = encoded.flatten()
    else:
        vector = np.zeros(COUNTRY_VECTOR_SIZE)
    return vector
