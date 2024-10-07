from config.config import PRODUCT_PROFILE_VECTOR_DIMENSION


product_schema = {
    "index": {
        "name": "product_index",
        "prefix": "product:",
        "storage_type": "json",
    },
    "fields": [
        {"name": "name", "type": "text"},
        {"name": "categories", "type": "tag"},
        {
            "name": "embeddings",
            "type": "vector",
            "attrs": {
                "dims": PRODUCT_PROFILE_VECTOR_DIMENSION,
                "distance_metric": "COSINE",
                "algorithm": "HNSW",
                "datatype": "FLOAT32"
            }
        }
    ],
}