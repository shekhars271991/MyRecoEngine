import redis
from redis.exceptions import RedisError, ConnectionError
from redisvl.index import SearchIndex
from redisvl.query import VectorQuery
from redisvl.query.filter import Tag, Num
import numpy as np
from config import MOVIE_PROFILE_VECTOR_DIMENSION

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
movie_schema = {
    "index": {
        "name": "movie_index",
        "prefix": "movie:",
        "storage_type": "json",
    },
    "fields": [
        {"name": "genres", "type": "tag"},
        {"name": "release_year", "type": "numeric"},
        {
            "name": "embeddings",
            "type": "vector",
            "attrs": {
                "dims": MOVIE_PROFILE_VECTOR_DIMENSION,
                "distance_metric": "COSINE",
                "algorithm": "HNSW",
                "datatype": "FLOAT32"
            }
        }
    ],
}

# Create the SearchIndex instance with exception handling
try:
    movie_index = SearchIndex.from_dict(movie_schema)
    movie_index.set_client(redis_client)
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

def search_movies_by_vector(query_vector, num_results=10):
    """
    Performs a vector search on the movie index.

    :param query_vector: Numpy array representing the query vector.
    :param num_results: Number of results to return.
    :return: List of matching movies.
    """
    try:
        # Convert the query vector to bytes
        vector = np.array(query_vector, dtype=np.float32).tobytes()

        # Create a VectorQuery
        vq = VectorQuery(
            vector=vector,
            vector_field_name="embeddings",
            return_fields=["release_year", "genres", "vector_score"],
            num_results=num_results
        )

        # Perform the query
        results = movie_index.query(vq)
        return results
    except (RedisError, ConnectionError) as e:
        print(f"Redis query failed: {e}")
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
            return_fields=["release_year", "genres", "vector_score"],
            filter_expression=filter_expression,
            num_results=num_results
        )

        # Perform the query
        results = movie_index.query(vq)
        return results
    except (RedisError, ConnectionError) as e:
        print(f"Redis query failed: {e}")
        raise

def initialize():
    """
    Initializes the movie index.
    """
    try:
        create_movie_index(overwrite=False)
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise
