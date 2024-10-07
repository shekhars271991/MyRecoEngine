from services.db.redis_service import getJson

from config.config import PRODUCT_PROFILE_VECTOR_DIMENSION

class Product:
    def __init__(self, product_id, name, description, categories, price, brand, features, release_date):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.categories = categories
        self.price = price
        self.brand = brand
        self.features = features
        self.release_date = release_date
        self.ratings = {} 

    @staticmethod
    def get_product_vector(product_id):
        
        product_key = f"{product_id}"
        product = getJson(product_key)
        if 'embeddings' in product:
            return product['embeddings']
        else:
            print(f"No embeddings found for movie_id {product_id}")
            return [0.0] * PRODUCT_PROFILE_VECTOR_DIMENSION
