import json
from redis_client import redis_client

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
        # Update logic based on feedback
        if watched:
            profile['watched'].append(movie_id)
            if rating:
                profile['ratings'][movie_id] = rating
        redis_client.json().set(self.profile_key, '.', profile)

    def _create_default_profile(self):
        default_profile = {
            'watched': [],
            'ratings': {},
            'feature_weights': [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]
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
        return {
            'title': redis_movie['title'].decode('utf-8'),
            'description': redis_movie['description'].decode('utf-8'),
            'cast': redis_movie['cast'].decode('utf-8')
        }
