PLOT_VECTOR_DIMENSION = 384  # Dimension of the embedding vector (for 'all-MiniLM-L6-v2' model)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
LEARNING_RATE = 0.5
NUM_RECO = 20
SIMILAR_USER_VECTOR_DISTANCE_THRESHOLD = 0.3
SIMILAR_MOVIE_VECTOR_DISTANCE_THRESHOLD = 0.3
CONTENT_BASED_RECO_COUNT = 5
from lookups import GENERES, ACTOR_CLUSTERS

GENRE_VECTOR_DIMENSION = len(GENERES)  
ACTOR_CLUSTERS_VECTOR_DIMENSION = len(ACTOR_CLUSTERS)
YEAR_VECTOR_DIMENSION = 1

MOVIE_PROFILE_VECTOR_DIMENSION = PLOT_VECTOR_DIMENSION + GENRE_VECTOR_DIMENSION + ACTOR_CLUSTERS_VECTOR_DIMENSION + YEAR_VECTOR_DIMENSION

PRODUCT_PROFILE_VECTOR_DIMENSION = 300

MOVIEDATA_FILEPATH= 'data/cleaned_movies_data.json'
PRODUCTS_DATA_FILEPATH = 'data/products/products.json'