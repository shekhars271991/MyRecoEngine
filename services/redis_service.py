import redis

# Redis client setup with byte responses
redis_client = redis.Redis(
    host= 'localhost',
    port='6379'
)

# def insert_movie_into_redis(movie):
#     movie_key = f"movie:{movie['title'].replace(' ', '_').lower()}"
    
#     # Insert the movie into Redis using hset
#     redis_client.hset(movie_key, mapping={
#         'title': movie['title'],
#         'description': movie['description'],
#         'cast': ', '.join(movie['cast']),
#         'release_year': movie['release_year']
#     })


def exists(key):
    return redis_client.exists(key)

def get_movie_from_redis(title):
    movie_key = f"movie:{title.replace(' ', '_').lower()}"
    movie_data = redis_client.hgetall(movie_key)
    
    if movie_data:
        # Convert the cast string back into a list
        movie_data['cast'] = movie_data['cast'].split(', ')
        return movie_data
    return None

def insert_movie(movie, movie_vector):
    """
    Inserts a movie into Redis using RedisJSON with the given embedding.
    If the movie already exists, it skips the insertion.

    :param movie: Dictionary containing movie data
    :param movie_vector: Numpy array representing the movie vector
    """
    # Generate the Redis key in the format 'movie:movie_title', with spaces replaced by underscores
    movie_title = movie.get('title', 'unknown_title').lower().replace(' ', '_')
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