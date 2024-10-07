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


def get_user_movie_profile(user):
    profile = redis_client.json().get(user.movie_profile_key)
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
    product_data['embeddings'] = product_vector.tolist()  # Convert NumPy array to list

    # Store the product data as a JSON document in Redis
    redis_client.json().set(product_key, '$', product_data)
    print(f"Product with SKU '{product['sku']}' inserted into Redis with key '{product_key}'.")


def get_all_products(page=1, page_size=10):
    """
    Retrieves all products from Redis with pagination.

    :param page: The page number (1-indexed).
    :param page_size: The number of products per page.
    :return: A tuple (products, total_products)
    """
    # Use SCAN to retrieve all product keys
    product_keys = []
    cursor = '0'
    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match='product:*', count=1000)
        product_keys.extend(keys)
        if cursor == 0 or cursor == '0':
            break

    # Total number of products
    total_products = len(product_keys)

    # Sort the keys to have consistent pagination
    product_keys.sort()

    # Calculate start and end indices for pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Slice the keys for the current page
    paginated_keys = product_keys[start_index:end_index]

    # Retrieve the products
    products = []
    for key in paginated_keys:
        key_str = key.decode('utf-8') if isinstance(key, bytes) else key
        product_data = redis_client.json().get(key_str)
        product_data.pop('embeddings', None)
        if product_data:
            products.append(product_data)

    return products, total_products


def get_user_product_profile(user):
    profile = redis_client.json().get(user.product_profile_key)
    return profile