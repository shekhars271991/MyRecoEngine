import requests
import json

# Load your movie data from the JSON file
with open('data/new/movie_list.json', 'r') as file:
    movies = json.load(file)

# API key and base URL for OMDB
api_key = "46d8a7da"
base_url = "https://omdbapi.com/?apikey=" + api_key + "&t="

# List to store updated movie data
updated_movies = []

# Loop through each movie, fetch data from OMDB, and update the movie data
for movie in movies:
    title = movie
    if title:  # Ensure the title exists
        response = requests.get(base_url + title)
        if response.status_code == 200:
            movie_data = response.json()
            if movie_data.get('Response') == 'True':  # Ensure the movie was found in OMDB
                 # Append OMDB details to the movie dictionary
                print(f"got data of : {movie}")
                updated_movies.append(movie_data)
            else:
                print(f"Movie not found on OMDB: {title}")
        else:
            print(f"Error fetching data for: {title}")
    else:
        print("No title found for one of the movies.")

# Save the updated data back to a new JSON file
with open('data/new/movies_data2.json', 'w') as outfile:
    json.dump(updated_movies, outfile, indent=4)

print("Updated movie data has been saved to 'movies_data2.json'.")
