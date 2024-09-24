import json
from services.redis_service import redis_client
import numpy as np
from config import MOVIE_PROFILE_VECTOR_DIMENSION, LEARNING_RATE
class Movie:
    @staticmethod
    
    def get_all_movies(user, page, page_size, status=None):
        """
        Fetch all movies without embeddings and categorize them into seen, not seen, and new.
        If status is provided, return only the specified section (seen, not seen, or new).
        """
        keys = redis_client.keys("movie:*")
        
        # Get user's profile to check watched and not watched actions
        profile = user.get_profile()

        # Get movies marked as watched and not watched from the user's profile
        watched_movies = profile.get('watched', [])
        ratings = profile.get('ratings', {})
        not_watched_movies = profile.get('not_watched', [])

        # Pagination logic
        total_movies = len(keys)
        start = (page - 1) * page_size
        end = start + page_size

        # Ensure page boundaries are within the range
        paginated_keys = keys[start:end]
        
        seen_movies = []
        not_seen_movies = []
        new_movies = []

        for key in paginated_keys:
            movie = redis_client.json().get(key)
            movie_id = key.decode("utf-8").split(":")[1]  # This extracts the part after "movie:"
            movie['id'] = movie_id

            if 'embeddings' in movie:
                movie.pop('embeddings')  # Remove embeddings

            # Categorize the movies
            if movie_id in watched_movies:
                movie['rating'] = ratings.get(movie_id, None)
                seen_movies.append(movie)
            elif movie_id in not_watched_movies:
                not_seen_movies.append(movie)
            else:
                new_movies.append(movie)

        # Filter based on status query param
        if status == 'seen':
            movies = seen_movies
        elif status == 'not_seen':
            movies = not_seen_movies
        elif status == 'new':
            movies = new_movies
        else:
            # Return all movies, categorized by seen, not_seen, and new
            movies = {
                'seen': seen_movies,
                'not_seen': not_seen_movies,
                'new': new_movies
            }

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
