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

def insert_movie(movie, embedding):
    """
    Inserts a movie into Redis using RedisJSON with the given embedding.

    :param movie: Dictionary containing movie data
    :param embedding: Numpy array representing the movie vector
    """
    movie_id = movie.get('title', 'unknown_title')  # Use title or another unique identifier as the key

    # Prepare the data to store
    movie_data = movie.copy()
    movie_data['embedding'] = embedding.tolist()  # Convert numpy array to list for JSON serialization

    # Store the movie data as a JSON document
    redis_client.json().set(movie_id, '$', movie_data)