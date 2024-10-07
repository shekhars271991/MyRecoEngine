# services/year_encoding_service.py
from config.movie_config import MIN_YEAR, MAX_YEAR
def get_year_normalized(release_year):
    """
    Normalizes the release year to a value between 0 and 1.

    :param release_year: The release year of the movie
    :param min_year: The minimum year in your dataset
    :param max_year: The maximum year in your dataset
    :return: A float representing the normalized year
    """
    if release_year:
        try:
            year = int(release_year)
            year_normalized = (year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)
            return [year_normalized]
        except ValueError:
            # Handle cases where release_year is not an integer
            return [0.0]
    else:
        return [0.0]
