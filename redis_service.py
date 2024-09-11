import redis

# Redis client setup with byte responses
redis_client = redis.Redis(
    host= 'localhost',
    port='6379'
)

def insert_movie_into_redis(movie):
    movie_key = f"movie:{movie['title'].replace(' ', '_').lower()}"
    
    # Insert the movie into Redis using hset
    redis_client.hset(movie_key, mapping={
        'title': movie['title'],
        'description': movie['description'],
        'cast': ', '.join(movie['cast']),
        'release_year': movie['release_year']
    })

def get_movie_from_redis(title):
    movie_key = f"movie:{title.replace(' ', '_').lower()}"
    movie_data = redis_client.hgetall(movie_key)
    
    if movie_data:
        # Convert the cast string back into a list
        movie_data['cast'] = movie_data['cast'].split(', ')
        return movie_data
    return None

