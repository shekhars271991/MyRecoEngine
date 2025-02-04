import redis
from redis.exceptions import RedisError, ConnectionError
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag, Num
import numpy as np
from schemas.movie import movie_schema
from schemas.user import user_schema

# Initialize the Redis client with exception handling
try:
    redis_client = redis.Redis(
        host='localhost',
        port=6379
    )
    # Test the connection
    redis_client.ping()
except (RedisError, ConnectionError) as e:
    print(f"Failed to connect to Redis: {e}")
    raise SystemExit(1)

# Define the movie index schema


# Create the SearchIndex instance with exception handling
try:
    movie_index = SearchIndex.from_dict(movie_schema)
    movie_index.set_client(redis_client)
    user_index = SearchIndex.from_dict(user_schema)
    user_index.set_client(redis_client)
except Exception as e:
    print(f"Failed to create SearchIndex instance: {e}")
    raise SystemExit(1)

def create_movie_index(overwrite=False):
    """
    Creates the movie index in Redis.
    :param overwrite: If True, overwrites the existing index.
    """
    try:
        movie_index.create(overwrite=overwrite)
        print("Movie index created successfully.")
    except Exception as e:
        print(f"Failed to create movie index: {e}")
        raise

def create_user_index(overwrite=False):
    """
    Creates the user index in Redis.
    :param overwrite: If True, overwrites the existing index.
    """
    try:
        user_index.create(overwrite=overwrite)
        print("User index created successfully.")
    except Exception as e:
        print(f"Failed to create user index: {e}")
        raise


def search_movies_by_vector_with_filters(query_vector, genres=None, min_year=None, max_year=None, num_results=10):
    """
    Performs a vector search with optional filters on genres and release year.

    :param query_vector: Numpy array representing the query vector.
    :param genres: List of genres to filter by.
    :param min_year: Minimum release year.
    :param max_year: Maximum release year.
    :param num_results: Number of results to return.
    :return: List of matching movies.
    """
    try:
        # Convert the query vector to bytes
        vector = np.array(query_vector, dtype=np.float32).tobytes()

        # Build filter expressions
        filters = []
        if genres:
            genre_filter = Tag("genres") == genres
            filters.append(genre_filter)
        if min_year is not None:
            year_filter_min = Num("release_year") >= min_year
            filters.append(year_filter_min)
        if max_year is not None:
            year_filter_max = Num("release_year") <= max_year
            filters.append(year_filter_max)

        # Combine filters if any
        filter_expression = None
        if filters:
            filter_expression = filters[0]
            for f in filters[1:]:
                filter_expression = filter_expression & f

        # Create a VectorQuery with filters
        vq = VectorQuery(
            vector=vector,
            vector_field_name="embeddings",
            # return_fields=["release_year", "genres", "vector_score"],
            filter_expression=filter_expression,
            num_results=num_results
        )

        # Perform the query
        results = movie_index.query(vq)
        return results
    except (RedisError, ConnectionError) as e:
        print(f"Redis query failed: {e}")
        raise


def search_similar_users(query_vector,num_results=10):
    try:
        # Convert the query vector to bytes
        vector = np.array(query_vector, dtype=np.float32).tobytes()
        # Create a VectorQuery
        vq = VectorQuery(
            vector=vector,
            vector_field_name="feature_weights",
            num_results=num_results
        )

        # Perform the query
        results = user_index.query(vq)
        return results
    
    except (RedisError, ConnectionError) as e:
        print(f"Failed to fetch similar users: {e}")
        raise


def initialize():
    """
    Initializes the movie and user index.
    """
    try:
        create_movie_index(overwrite=False)
        create_user_index(overwrite=False)
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise
