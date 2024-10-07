# create_product_vector.py

import numpy as np

from services.products.generate_embeddings.text_embedding_service import get_text_embedding
from services.products.generate_embeddings.categorical_encoding_service import (
    encode_categories,
    encode_features,
    encode_colors,
    encode_manufacturer
)
from services.products.generate_embeddings.numerical_scaling_service import scale_numerical_features

def create_product_vector(product):
    vectors = []

    # Text Embeddings
    TEXT_EMBEDDING_SIZE = 384  # Adjust according to your embedding model

    name_embedding = get_text_embedding(product.get('name', ''))
    if name_embedding is not None and len(name_embedding.shape) > 0:
        vectors.append(name_embedding)
    else:
        vectors.append(np.zeros(TEXT_EMBEDDING_SIZE))

    description_embedding = get_text_embedding(product.get('description', ''))
    if description_embedding is not None and len(description_embedding.shape) > 0:
        vectors.append(description_embedding)
    else:
        vectors.append(np.zeros(TEXT_EMBEDDING_SIZE))

    # Categorical Encodings
    categories_vector = encode_categories(product.get('categories', []))
    vectors.append(categories_vector)

    features_vector = encode_features(product.get('features', []))
    vectors.append(features_vector)

    colors_vector = encode_colors(product.get('color', []))
    vectors.append(colors_vector)

    manufacturer_vector = encode_manufacturer(product.get('manufacturer', ''))
    vectors.append(manufacturer_vector)

    # Numerical Features
    numerical_vector = scale_numerical_features(product)
    vectors.append(numerical_vector)

    # Combine All Vectors
    product_vector = np.concatenate(vectors)
    return product_vector
