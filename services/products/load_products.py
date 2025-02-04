import numpy as np
from config import PRODUCT_PROFILE_VECTOR_DIMENSION
from services.products.description_embedding_service import get_description_embeddings
from services.db.redis_service import insert_product

def create_product_vector(product):
    """
    Create a feature vector for a product based on its attributes
    Args:
        product (dict): Product data containing description, price, rating, etc.
    Returns:
        numpy.ndarray: The combined feature vector
    """
    vectors = []
    
    # Product Description Embedding
    description = product.get('description', '')
    if description:
        description_embedding = get_description_embeddings(description)
        vectors.append(description_embedding)
    else:
        vectors.append(np.zeros(PRODUCT_PROFILE_VECTOR_DIMENSION))
    
    # Price Normalization (simple min-max scaling assuming price range 0-10000)
    price = float(product.get('price', 0))
    price_normalized = min(max(price / 10000.0, 0), 1)
    vectors.append(np.array([price_normalized]))
    
    # Rating Normalization (0-5 scale)
    rating = float(product.get('rating', 0))
    rating_normalized = min(max(rating / 5.0, 0), 1)
    vectors.append(np.array([rating_normalized]))
    
    # Stock level normalization (0-1000 scale)
    stock = int(product.get('stock', 0))
    stock_normalized = min(max(stock / 1000.0, 0), 1)
    vectors.append(np.array([stock_normalized]))
    
    # Combine all vectors
    product_vector = np.concatenate(vectors)
    return product_vector

def load_product_data(product):
    """
    Load a single product into Redis with its feature vector
    Args:
        product (dict): Product data containing id, name, description, price, etc.
    """
    try:
        # Create the product vector
        product_vector = create_product_vector(product)
        
        # Store the product data in Redis using insert_product
        insert_product(product, product_vector)
        
    except KeyError as e:
        raise Exception(f"Missing required field in product data: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading product data: {str(e)}")
