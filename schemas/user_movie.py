from config.config import MOVIE_PROFILE_VECTOR_DIMENSION
user_movie_schema = {
    "index": {
        "name": "user_movie_index",
        "prefix": "movie_profile:",
        "storage_type": "json",
    },
    "fields": [
        {
            "name": "feature_weights",
            "type": "vector",
            "attrs": {
                "dims": MOVIE_PROFILE_VECTOR_DIMENSION,
                "distance_metric": "COSINE",
                "algorithm": "HNSW",
                "datatype": "FLOAT32"
            }
        }
    ],
}