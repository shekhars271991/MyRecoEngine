
import numpy as np
from config import MOVIE_PROFILE_VECTOR_DIMENSION
from services.movies.plot_encoding_service import get_plot_embeddings
from services.movies.genre_encoding_service import get_genre_vector
from services.movies.actor_encoding_service import get_cast_encoding, CLUSTER_VECTOR_SIZE
from services.movies.release_year_encoding_service import get_year_normalized 
from services.db.redis_service import insert_movie

def create_movie_vector(movie):
    vectors = []
    
    # Plot Description Embedding
    plot_description = movie.get('description', '')
    if plot_description:
        plot_embedding = get_plot_embeddings(plot_description)
        vectors.append(plot_embedding)
    else:
        vectors.append(np.zeros(MOVIE_PROFILE_VECTOR_DIMENSION))
    
    # Genre Encoding 
    genres = movie.get('genres', [])
    genre_vector = get_genre_vector(genres)
    vectors.append(genre_vector)
    
    # Cast Encoding using cluster-based approach
    cast_members = movie.get('actors', [])
    if cast_members:
        cast_vector = get_cast_encoding(cast_members)
        vectors.append(cast_vector)
    else:
        vectors.append(np.zeros(CLUSTER_VECTOR_SIZE))
    
    # Release Year Normalization 
    release_year = movie.get('release_year')
    year_vector = get_year_normalized(release_year)
    vectors.append(year_vector)
    
    # Combine all vectors
    movie_vector = np.concatenate(vectors)
    return movie_vector

def load_movie_data(movie):
    # Compute the full movie vector
    movie_vector = create_movie_vector(movie)
    
    # Insert the updated movie (with the embedding) into Redis
    insert_movie(movie, movie_vector)
