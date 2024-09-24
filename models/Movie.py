import json
from services.redis_service import redis_client
import numpy as np
from config import MOVIE_PROFILE_VECTOR_DIMENSION, LEARNING_RATE
class Movie:
    @staticmethod
    def get_all_movies(page, page_size):
        """
        Fetch all movies without embeddings and with pagination.
        """
        keys = redis_client.keys("movie:*")
        
        # Pagination logic
        total_movies = len(keys)
        start = (page - 1) * page_size
        end = start + page_size

        # Ensure page boundaries are within the range
        paginated_keys = keys[start:end]
        
        movies = []
        for key in paginated_keys:
            movie = redis_client.json().get(key)
            if 'embeddings' in movie:
                movie.pop('embeddings')  # Remove embeddings
            movies.append(movie)

        return movies, total_movies

    @staticmethod
    def get_movie_vector(movie_id):
        """
        Fetch the movie's plot vector from Redis.
        Assume the plot vector is stored as "movie:<id>:vector" in Redis.
        """
        movie_key = f"movie:{movie_id}"
        movie = redis_client.json().get(movie_key)
        if 'embeddings' in movie:
            return movie['embeddings']
        else:
            print(f"No embeddings found for movie_id {movie_id}")
            return [0.0] * MOVIE_PROFILE_VECTOR_DIMENSION 
