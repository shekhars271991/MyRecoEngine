# models.py

import json
from redis_service import redis_client
import numpy as np
from config import VECTOR_DIMENSION, LEARNING_RATE
class User:
    def __init__(self, username):
        self.username = username
        self.profile_key = f"user:{self.username}:profile"

    def get_profile(self):
        profile = redis_client.json().get(self.profile_key)
        return profile if profile else self._create_default_profile()

    def update_movie_status(self, movie_id, watched, rating=None):
        # Update the user profile based on watched status and rating
        profile = self.get_profile()
        
        # Ensure 'watched' and 'ratings' are initialized
        if 'watched' not in profile or not isinstance(profile['watched'], list):
            profile['watched'] = []
        if 'ratings' not in profile or not isinstance(profile['ratings'], dict):
            profile['ratings'] = {}

        is_movie_watched = movie_id in profile['watched']

        if watched:
            # User wants to mark the movie as watched
            if not is_movie_watched:
                # Add movie to 'watched' list
                profile['watched'].append(movie_id)
                print(f"Movie {movie_id} added to watched list.")
            else:
                print(f"Movie {movie_id} is already in the watched list.")
            
            if rating is not None:
                # Update or set the rating
                profile['ratings'][movie_id] = rating
                # Fetch the movie's plot vector
                movie_vector = Movie.get_movie_vector(movie_id)
                # Update the user's feature vector based on rating and movie vector
                profile['feature_weights'] = self._update_profile_vector(
                    profile['feature_weights'], movie_vector, rating
                )
            else:
                if movie_id in profile['ratings']:
                    # Keep existing rating
                    print(f"No new rating provided for movie {movie_id}. Existing rating retained.")
                else:
                    # No rating provided, and none exists
                    print(f"No rating provided for movie {movie_id}.")
        else:
            # User wants to mark the movie as not watched
            if is_movie_watched:
                # Remove movie from 'watched' list
                profile['watched'].remove(movie_id)
                # Remove rating if exists
                if movie_id in profile['ratings']:
                    del profile['ratings'][movie_id]
                # Adjust 'feature_weights' accordingly
                profile['feature_weights'] = self._recalculate_feature_weights(profile)
                print(f"Movie {movie_id} removed from watched list.")
            else:
                print(f"Movie {movie_id} is already not in the watched list.")
                if rating is not None:
                    # Cannot rate a movie that is not watched 
                    raise ValueError("Cannot rate a movie that is not marked as watched.")
                # Else, do nothing

        # Save the updated profile back to Redis
        redis_client.json().set(self.profile_key, '.', profile)

    def _update_profile_vector(self, profile_vector, movie_vector, rating):
        # Normalize rating (assuming rating is between 1 and 5)
        weight_factor = rating / 5.0
        alpha = LEARNING_RATE  # Learning rate

        # Convert lists to numpy arrays for vectorized computation
        profile_vector = np.array(profile_vector)
        movie_vector = np.array(movie_vector)

        # Update the profile vector based on the formula
        new_profile_vector = (1 - alpha) * profile_vector + alpha * weight_factor * movie_vector

        # Normalize the new profile vector
        norm = np.linalg.norm(new_profile_vector)
        if norm > 0:
            new_profile_vector = new_profile_vector / norm

        return new_profile_vector.tolist()

    def _recalculate_feature_weights(self, profile):
        # Recalculate feature_weights based on remaining watched movies and their ratings
        watched_movie_ids = profile['watched']
        ratings = profile['ratings']

        if not watched_movie_ids:
            # No movies watched, reset feature_weights to default
            return self._create_default_profile()['feature_weights']

        total_weight = 0.0
        cumulative_vector = np.zeros(len(profile['feature_weights']))
        for movie_id in watched_movie_ids:
            rating = ratings.get(movie_id, 3)  # Assume default rating of 3 if not rated
            weight_factor = rating / 5.0
            movie_vector = np.array(Movie.get_movie_vector(movie_id))
            cumulative_vector += weight_factor * movie_vector
            total_weight += weight_factor

        if total_weight > 0:
            new_feature_weights = cumulative_vector / total_weight
            # Normalize the new feature weights
            norm = np.linalg.norm(new_feature_weights)
            if norm > 0:
                new_feature_weights = new_feature_weights / norm
            return new_feature_weights.tolist()
        else:
            return self._create_default_profile()['feature_weights']

    def _create_default_profile(self):
        default_profile = {
            'watched': [],
            'ratings': {},
            'feature_weights': [0.0] * VECTOR_DIMENSION  # Zero vector
        }
        redis_client.json().set(self.profile_key, '.', default_profile)
        return default_profile

    def get_vector(self):
        profile = self.get_profile()
        return profile['feature_weights']

class Movie:
    @staticmethod
    def get_all_movies():
        keys = redis_client.keys("movie:*")
        movies = []
        for key in keys:
            movie = redis_client.json().get(key)
            movies.append(movie)
        return movies

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
            return [0.0] * VECTOR_DIMENSION  # Replace with your actual embedding dimension
