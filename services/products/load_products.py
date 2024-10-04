
# def create_product_vector(product):
#     vectors = []
    
#     # Description Embedding
#     description = product.description
#     if description:
#         description_embedding = get_description_embeddings(description)
#         vectors.append(description_embedding)
#     else:
#         vectors.append(np.zeros(DESCRIPTION_VECTOR_DIMENSION))
    
#     # Category Encoding
#     categories_vector = get_category_vector(product.categories)
#     vectors.append(categories_vector)
    
#     # Brand Encoding
#     brand_vector = get_brand_vector(product.brand)
#     vectors.append(brand_vector)
    
#     # Feature Encoding
#     features_vector = get_features_vector(product.features)
#     vectors.append(features_vector)
    
#     # Price Normalization
#     price_vector = get_price_normalized(product.price)
#     vectors.append(price_vector)
    
#     # Release Date Encoding
#     date_vector = get_date_normalized(product.release_date)
#     vectors.append(date_vector)
    
#     # Combine all vectors
#     product_vector = np.concatenate(vectors)
#     return product_vector


# def load_product_data(product):
#     # Compute the full product vector
#     product_vector = create_product_vector(product)
    
#     # Insert the product (with the embedding) into Redis or your database
#     insert_product(product, product_vector)
