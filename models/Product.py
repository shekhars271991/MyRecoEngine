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