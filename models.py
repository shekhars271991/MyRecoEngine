import json
from redis_service import redis_client

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
        
        # If the movie is watched, update the status and rating
        if watched:
            profile['watched'].append(movie_id)
            if rating:
                profile['ratings'][movie_id] = rating
                # Fetch the movie's plot vector (assume we store it as "movie:<id>:vector")
                movie_plot_vector = Movie.get_movie_vector(movie_id)
                # Update the user's feature vector based on rating and plot vector
                profile['feature_weights'] = self._update_profile_vector(profile['feature_weights'], movie_plot_vector, rating)

        # Save the updated profile back to Redis
        redis_client.json().set(self.profile_key, '.', profile)

    def _update_profile_vector(self, profile_vector, movie_vector, rating):
        # Normalize rating (assuming rating is between 1 and 5)
        weight_factor = rating / 5.0
        alpha = 0.5  # Learning rate

        # Update the profile vector based on the formula
        new_profile_vector = [
            (1 - alpha) * pv + alpha * weight_factor * mv
            for pv, mv in zip(profile_vector, movie_vector)
        ]

        return new_profile_vector

    def _create_default_profile(self):
        default_profile = {
            'watched': [],
            'ratings': {},
            'feature_weights': [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]  # Initial default profile vector
        }
        redis_client.json().set(self.profile_key, '.', default_profile)
        return default_profile


class Movie:
    @staticmethod
    def get_all_movies():
        keys = redis_client.keys("movie:*")
        movies = []
        for key in keys:
            movie = redis_client.hgetall(key)
            movies.append(Movie.from_redis(movie))
        return movies

    @staticmethod
    def from_redis(redis_movie):
        try:
            return {
                'title': redis_movie.get(b'title', b'').decode('utf-8'),
                'description': redis_movie.get(b'description', b'').decode('utf-8'),
                'cast': redis_movie.get(b'cast', b'').decode('utf-8'),
                'releaseYear': redis_movie.get(b'release_year', b'').decode('utf-8'),
            }
        except KeyError as e:
            print(f"KeyError: {e} is missing in redis_movie: {redis_movie}")
            return {}

    @staticmethod
    def get_movie_vector(movie_id):
        """
        Fetch the movie's plot vector from Redis.
        Assume the plot vector is stored as "movie:<id>:vector" in Redis.
        """
        
        movie = redis_client.json().get(movie_id)
        return movie['embeddings']
        # if movie_vector:
        #     return movie_vector
        # else:
        #     print(f"No vector found for movie_id {movie_id}")
        #     return [0] * 6  # Assuming a 6-dimensional vector, replace with your actual dimensions
