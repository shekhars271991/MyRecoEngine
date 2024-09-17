# services/actor_encoding_service.py

import numpy as np
from lookups import ACTOR_CLUSTERS

# Define clusters for Hollywood actors based on their career paths and specializations

# Create a vector mapping for each cluster
CLUSTER_VECTORS = {}
cluster_names = list(ACTOR_CLUSTERS.keys())
for idx, cluster in enumerate(cluster_names):
    vector = np.zeros(len(ACTOR_CLUSTERS))
    vector[idx] = 1
    CLUSTER_VECTORS[cluster] = vector

# Define the cluster vector size
CLUSTER_VECTOR_SIZE = len(ACTOR_CLUSTERS)

def get_actor_vector(actor_name):
    """
    Returns the encoding vector for the actor based on the predefined clusters.
    
    If the actor does not belong to any predefined cluster, return a zero vector.
    """
    for cluster, actors in ACTOR_CLUSTERS.items():
        if actor_name in actors:
            return CLUSTER_VECTORS[cluster]
    
    # Return a zero vector if actor is not found in any cluster
    return np.zeros(CLUSTER_VECTOR_SIZE)

def get_cast_encoding(cast_list):
    """
    Returns the vector encoding for a list of cast members by averaging their individual encodings.
    
    :param cast_list: List of actor names in the movie's cast
    :return: Vector representing the encoding for the cast
    """
    if not cast_list:
        return np.zeros(CLUSTER_VECTOR_SIZE)  # Return a zero vector if no cast is provided
    
    cast_vectors = []
    for actor in cast_list:
        cast_vectors.append(get_actor_vector(actor))
    
    if cast_vectors:
        return np.mean(cast_vectors, axis=0)
    else:
        return np.zeros(CLUSTER_VECTOR_SIZE)
