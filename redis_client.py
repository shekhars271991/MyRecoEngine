import redis

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
