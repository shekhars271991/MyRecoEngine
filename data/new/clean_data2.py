import json

def clean_movie_data(movie):
    cleaned_movie = {}
    
    # Define fields to convert comma-separated strings into arrays
    fields_to_convert_to_array = ["actors", "language", "writer", "genre"]
    
    for key, value in movie.items():
        # Convert the key to lowercase
        new_key = key.lower()

        # Convert Year to number
        if new_key == "year":
            try:
                cleaned_movie[new_key] = int(value)
            except (ValueError, TypeError):
                cleaned_movie[new_key] = value  # If it's not convertible, keep it as is

        # Convert comma-separated fields to arrays
        elif new_key in fields_to_convert_to_array and isinstance(value, str):
            cleaned_movie[new_key] = [item.strip() for item in value.split(",")]

        # Directly assign the value for other fields
        else:
            cleaned_movie[new_key] = value
    
    return cleaned_movie

# Load movie data from a JSON file
with open('data/new/movies_data2.json', 'r') as file:
    movies = json.load(file)

cleaned_movies = []
for i, movie in enumerate(movies):
    try:
        cleaned_movie = clean_movie_data(movie)
        cleaned_movies.append(cleaned_movie)
    except Exception as e:
        print(f"Error processing movie at index {i}: {e}")

# Save the cleaned data back to a new JSON file
with open('data/new/cleaned_movies_data2.json', 'w') as outfile:
    json.dump(cleaned_movies, outfile, indent=4)

print("Cleaned movie data has been saved to 'cleaned_movies_data2.json'.")
