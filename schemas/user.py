from config.config import MOVIE_PROFILE_VECTOR_DIMENSION
user_schema = {
    "index": {
        "name": "user_index",
        "prefix": "profile:",
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