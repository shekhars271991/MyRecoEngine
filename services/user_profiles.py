import json
from services.redis_service import redis_client

# Get user profile (returns feature vector)
def get_user_profile(user):
    profile = redis_client.json().get(user.profile_key)
    return profile['feature_weights']

# Update user profile based on feedback
def update_user_profile(user, feedback):
    # Modify profile based on watched, rating, and feedback
    pass
