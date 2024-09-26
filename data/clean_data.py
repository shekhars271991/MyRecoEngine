import json

def clean_movie_data(movie):
    cleaned_movie = {}
    
    # Define fields to convert comma-separated strings into arrays
    fields_to_convert_to_array = ["actors", "language", "writer"]
    
    for key, value in movie.items():
        # Convert the key to lowercase
        new_key = key.lower()
        if new_key == "cast":
            continue 
        # Remove "genre" field if "genres" exists
        if new_key == "genre" and "genres" in movie:
            continue  # Skip this field

        # Convert Year to number
        if new_key == "year":
            try:
                cleaned_movie[new_key] = int(value)
            except ValueError:
                cleaned_movie[new_key] = value  # If it's not convertible, keep it as is

        # Convert comma-separated fields to arrays
        elif new_key in fields_to_convert_to_array and isinstance(value, str):
            cleaned_movie[new_key] = [item.strip() for item in value.split(",")]

        # Directly assign the value for other fields
        else:
            cleaned_movie[new_key] = value
    
    return cleaned_movie

# Load movie data from a JSON file
with open('data/updated_movies_data.json', 'r') as file:
    movies = json.load(file)

# Clean the movies by removing redundant fields and applying the transformations
cleaned_movies = [clean_movie_data(movie) for movie in movies]

# Save the cleaned data back to a new JSON file
with open('data/cleaned_movies_data.json', 'w') as outfile:
    json.dump(cleaned_movies, outfile, indent=4)

print("Cleaned movie data has been saved to 'cleaned_movies_data.json'.")
