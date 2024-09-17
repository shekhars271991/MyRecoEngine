import numpy as np

MIN_YEAR = 1900  
MAX_YEAR = 2023 
GENERES =  [
    'Action',
    'Adventure',
    'Animation',
    'Biography',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Family',
    'Fantasy',
    'History',
    'Horror',
    'Music',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Sport',
    'Thriller',
    'War',
    'Western'
] 

# Define clusters for Hollywood actors based on their career paths and specializations
ACTOR_CLUSTERS = {
    "Action Stars": ["Arnold Schwarzenegger", "Sylvester Stallone", "Bruce Willis", "Tom Cruise", "Keanu Reeves"],
    "Drama Experts": ["Marlon Brando", "Al Pacino", "Robert De Niro", "Leonardo DiCaprio", "Morgan Freeman"],
    "Comedic Actors": ["Jim Carrey", "Will Ferrell", "Steve Carell", "Eddie Murphy", "Adam Sandler"],
    "Sci-Fi Regulars": ["Keanu Reeves", "Sigourney Weaver", "Tom Cruise", "Harrison Ford", "Carrie Fisher"],
    "Tarantino Collaborators": ["Samuel L. Jackson", "Uma Thurman", "John Travolta", "Harvey Keitel", "Christoph Waltz"],
    "Nolan Collaborators": ["Christian Bale", "Michael Caine", "Tom Hardy", "Joseph Gordon-Levitt", "Cillian Murphy"],
    "Fantasy Stars": ["Elijah Wood", "Ian McKellen", "Viggo Mortensen", "Orlando Bloom", "Cate Blanchett"]
}

