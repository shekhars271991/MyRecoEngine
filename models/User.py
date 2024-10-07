from services.db.redis_service import redis_client
import numpy as np
from config.config import LEARNING_RATE, MOVIE_PROFILE_VECTOR_DIMENSION, PRODUCT_PROFILE_VECTOR_DIMENSION
from models.Movie import Movie
from models.Product import Product

class User:
    def __init__(self, username):
        self.username = username
        self.movie_profile_key = f"profile:{self.username}"
        self.product_profile_key = f"product_profile:{self.username}"

    ### Movie-related Methods (Unchanged) ###

    def get_profile(self):
        profile = redis_client.json().get(self.movie_profile_key)
        return profile if profile else self._create_default_movie_profile()

    def update_movie_status(self, movie_id, watched, rating=None):
        """
        Update the user movie profile based on watched/not watched status and rating.
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
                profile['feature_weights'] = self._update_movie_profile_vector(
                    profile['feature_weights'], movie_vector, rating
                )
        else:
            # Mark movie as not watched
            if is_movie_watched:
                profile['watched'].remove(movie_id)
                if movie_id in profile['ratings']:
                    del profile['ratings'][movie_id]  # Remove rating if exists
                # Optionally recalculate feature weights here
            if not is_movie_not_watched:
                profile['not_watched'].append(movie_id)

        # Save the updated profile back to Redis
        redis_client.json().set(self.movie_profile_key, '.', profile)

    def _update_movie_profile_vector(self, profile_vector, movie_vector, rating):
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

    def _create_default_movie_profile(self):
        default_profile = {
            'watched': [],
            'not_watched': [],
            'ratings': {},
            'feature_weights': [0.0] * MOVIE_PROFILE_VECTOR_DIMENSION  # Zero vector
        }
        redis_client.json().set(self.movie_profile_key, '.', default_profile)
        return default_profile

    def get_movie_vector(self):
        profile = self.get_profile()
        return profile['feature_weights']

    ### Product-related Methods ###

    def get_product_profile(self):
        profile = redis_client.json().get(self.product_profile_key)
        return profile if profile else self._create_default_product_profile()

    def rate_product(self, product_id, rating):
        """
        Updates the user product profile based on product rating.

        :param product_id: The ID or SKU of the product.
        :param rating: The user's rating of the product (e.g., between 1 and 5).
        """
        profile = self.get_product_profile()
        
        # Ensure 'ratings' and 'rated_products' are initialized
        if 'ratings' not in profile or not isinstance(profile['ratings'], dict):
            profile['ratings'] = {}
        if 'rated_products' not in profile or not isinstance(profile['rated_products'], list):
            profile['rated_products'] = []

        # Update or set the rating
        profile['ratings'][product_id] = rating
        if product_id not in profile['rated_products']:
            profile['rated_products'].append(product_id)
        
        # Get the product vector
        product_vector = Product.get_product_vector(product_id)
        if product_vector is None:
            raise ValueError(f"Product vector for product ID '{product_id}' not found.")
        
        # Update the user's product profile vector
        profile['feature_weights'] = self._update_product_profile_vector(
            profile['feature_weights'], product_vector, rating
        )

        # Save the updated profile back to Redis
        redis_client.json().set(self.product_profile_key, '.', profile)

    def _update_product_profile_vector(self, profile_vector, product_vector, rating):
        # Normalize rating (assuming rating is between 1 and 5)
        weight_factor = rating / 5.0
        alpha = LEARNING_RATE  # Learning rate

        # Convert lists to numpy arrays for vectorized computation
        profile_vector = np.array(profile_vector)
        product_vector = np.array(product_vector)

        # Ensure both vectors have the same shape
        if profile_vector.shape != product_vector.shape:
            raise ValueError(f"Profile vector shape {profile_vector.shape} does not match product vector shape {product_vector.shape}")
        
        # Update the profile vector based on the formula
        new_profile_vector = (1 - alpha) * profile_vector + alpha * weight_factor * product_vector

        # Normalize the new profile vector
        norm = np.linalg.norm(new_profile_vector)
        if norm > 0:
            new_profile_vector = new_profile_vector / norm

        return new_profile_vector.tolist()

    def _create_default_product_profile(self):
        default_profile = {
            'rated_products': [],
            'ratings': {},
            'feature_weights': [0.0] * PRODUCT_PROFILE_VECTOR_DIMENSION  # Zero vector
        }
        redis_client.json().set(self.product_profile_key, '.', default_profile)
        return default_profile

    def get_product_vector(self):
        profile = self.get_product_profile()
        return profile['feature_weights']
