from config.config import PRODUCT_PROFILE_VECTOR_DIMENSION

user_product_schema = {
    "index": {
        "name": "user_product_index",
        "prefix": "product_profile:",
        "storage_type": "json",
    },
    "fields": [
        {
            "name": "feature_weights",
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