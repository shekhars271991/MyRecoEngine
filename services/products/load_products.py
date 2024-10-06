# load_products.py

from services.products.product_vector_service import create_product_vector
from services.db.redis_service import insert_product 

# Define load_all_products which handles loading, fitting, and storing products
def load_all_products(products):
    for product in products:
        # Generate the product vector
        product_vector = create_product_vector(product)
        insert_product(product, product_vector)
