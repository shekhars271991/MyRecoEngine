from services.redis_service import redis_client
import numpy as np
from config import LEARNING_RATE, MOVIE_PROFILE_VECTOR_DIMENSION
from models.Movie import Movie
class User:
    def __init__(self, username):
        self.username = username
        self.profile_key = f"profile:{self.username}"

    def get_profile(self):
        profile = redis_client.json().get(self.profile_key)
        return profile if profile else self._create_default_profile()


    def update_movie_status(self, movie_id, watched, rating=None):
        """
        Update the user profile based on watched/not watched status and rating.
        """
        profile = self.get_profile()
        
        # Ensure 'watched', 'not_watched', and 'ratings' are initialized
        if 'watched' not in profile or not isinstance(profile['watched'], list):
            profile['watched'] = []
        if 'ratings' not in profile or not isinstance(profile['ratings'], dict):
            profile['ratings'] = {}
        if 'not_watched' not in profile or not isinstance(profile['not_watched'], list):
            profile['not_watched'] = []

        is_movie_watched = movie_id in profile['watched']
        is_movie_not_watched = movie_id in profile['not_watched']

        if watched:
            # Mark movie as watched
            if not is_movie_watched:
                profile['watched'].append(movie_id)
                if is_movie_not_watched:
                    profile['not_watched'].remove(movie_id)  # Remove from not_watched if it exists
            if rating is not None:
                # Update or set the rating
                profile['ratings'][movie_id] = rating
                movie_vector = Movie.get_movie_vector(movie_id)
                profile['feature_weights'] = self._update_profile_vector(
                    profile['feature_weights'], movie_vector, rating
                )
        else:
            # Mark movie as not watched
            if is_movie_watched:
                profile['watched'].remove(movie_id)
                if movie_id in profile['ratings']:
                    del profile['ratings'][movie_id]  # Remove rating if exists
                # profile['feature_weights'] = self._recalculate_feature_weights(profile)
            if not is_movie_not_watched:
                profile['not_watched'].append(movie_id)

        # Save the updated profile back to Redis
        redis_client.json().set(self.profile_key, '.', profile)


    def _update_profile_vector(self, profile_vector, movie_vector, rating):
        # Normalize rating (assuming rating is between 1 and 5)
        weight_factor = rating / 5.0
        alpha = LEARNING_RATE  # Learning rate

        # Convert lists to numpy arrays for vectorized computation
        profile_vector = np.array(profile_vector)
        movie_vector = np.array(movie_vector)

        # Ensure both vectors have the same shape
        if profile_vector.shape != movie_vector.shape:
            raise ValueError(f"Profile vector shape {profile_vector.shape} does not match movie vector shape {movie_vector.shape}")
        
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
        cumulative_vector = np.zeros(MOVIE_PROFILE_VECTOR_DIMENSION)
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
            'feature_weights': [0.0] * MOVIE_PROFILE_VECTOR_DIMENSION  # Zero vector
        }
        redis_client.json().set(self.profile_key, '.', default_profile)
        return default_profile

    def get_vector(self):
        profile = self.get_profile()
        return profile['feature_weights']
