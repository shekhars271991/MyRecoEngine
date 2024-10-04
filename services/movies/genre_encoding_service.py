# services/genre_encoding_service.py

import numpy as np
from sklearn.preprocessing import OneHotEncoder
from lookups import GENERES

# Initialize OneHotEncoder for genres
all_genres = GENERES

genre_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
genre_encoder.fit(np.array(all_genres).reshape(-1, 1))

def get_genre_vector(genres):
    """
    Encodes the list of genres into a one-hot encoded vector.
    If genres is empty, returns a zero vector of appropriate size.
    
    :param genres: List of genres for the movie
    :return: Numpy array representing the genre vector
    """
    if genres:
        genres_encoded = genre_encoder.transform(np.array(genres).reshape(-1, 1))
        # Sum over genres to get a single vector
        genre_vector = np.sum(genres_encoded, axis=0)
    else:
        genre_vector = np.zeros(len(all_genres))
    return genre_vector
