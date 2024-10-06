import redis

# Redis client setup with byte responses
redis_client = redis.Redis(
    host= 'localhost',
    port='6379'
)


def exists(key):
    return redis_client.exists(key)



def insert_movie(movie, movie_vector):
    """
    Inserts a movie into Redis using RedisJSON with the given embedding.
    If the movie already exists, it skips the insertion.

    :param movie: Dictionary containing movie data
    :param movie_vector: Numpy array representing the movie vector
    """
    # Generate the Redis key in the format 'movie:movie_title', with spaces replaced by underscores
    movie_title = movie.get('title', 'unknown_title').lower().replace(' ', '_').replace(':','_')
    movie_key = f"movie:{movie_title}"

    # Check if the movie already exists in Redis
    if redis_client.exists(movie_key):
        print(f"Movie '{movie.get('title')}' already exists in Redis. Skipping insertion.")
        return

    # Prepare the data to store
    movie_data = movie.copy()
    movie_data['embeddings'] = movie_vector.tolist()

    # Store the movie data as a JSON document
    redis_client.json().set(movie_key, '$', movie_data)
    print(f"Movie '{movie.get('title')}' inserted into Redis with key '{movie_key}'.")


def getJson(key):
    return redis_client.json().get(key)


def get_user_profile(user):
    profile = redis_client.json().get(user.profile_key)
    return profile


def insert_product(product, product_vector):
    """
    Inserts a product into Redis using RedisJSON with the given vector.
    If the product already exists, it skips the insertion.

    :param product: Dictionary containing product data.
    :param product_vector: Numpy array representing the product vector.
    """
    # Generate the Redis key in the format 'product:sku'
    product_key = f"product:{product['sku']}"

    # Check if the product already exists in Redis
    if redis_client.exists(product_key):
        print(f"Product with SKU '{product['sku']}' already exists in Redis. Skipping insertion.")
        return

    # Prepare the data to store
    product_data = product.copy()
    product_data['vector'] = product_vector.tolist()  # Convert NumPy array to list

    # Store the product data as a JSON document in Redis
    redis_client.json().set(product_key, '$', product_data)
    print(f"Product with SKU '{product['sku']}' inserted into Redis with key '{product_key}'.")