from config.config import MOVIE_PROFILE_VECTOR_DIMENSION
movie_schema = {
    "index": {
        "name": "movie_index",
        "prefix": "movie:",
        "storage_type": "json",
    },
    "fields": [
        {"name": "genres", "type": "tag"},
        {"name": "release_year", "type": "numeric"},
        {
            "name": "embeddings",
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