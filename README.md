Movie Recommendation API
========================

This project is a Flask-based backend API for a movie recommendation system. It supports user registration, login, fetching movie data, movie recommendations, and similar user-based recommendations. The project also includes functionality to load movie data from a JSON file into Redis.

Features
--------

-   **User Registration & Login**: Register users and authenticate using JWT tokens.
-   **Movie List**: Fetch paginated movie lists with filters for "seen", "not seen", or "new".
-   **Movie Actions**: Mark movies as watched/not watched and rate them.
-   **Recommendations**: Get movie recommendations based on your viewing preferences.
-   **Similar Users**: Get similar user profiles based on movie watching behavior.
-   **Load Movies**: Load movie data into Redis from a JSON file.

Table of Contents
-----------------

-   [Installation](#installation)
-   [API Routes](#api-routes)
-   [Environment Variables](#environment-variables)
-   [Running the Application](#running-the-application)
-   [Movie Data](#movie-data)

Installation
------------

Follow these steps to set up and run the project on your local machine:

### Prerequisites

-   Python 3.7 or later
-   Redis server
-   [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

### Steps

1.  **Clone the Repository**

    bash

    Copy code

    `git clone <repository-url>
    cd movie-recommendation-backend`

2.  **Set Up Virtual Environment**

    bash

    Copy code

    `python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate`

3.  **Install Dependencies**

    Install the required Python packages by running:

    bash

    Copy code

    `pip install -r requirements.txt`

4.  **Set Up Environment Variables**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    bash

    Copy code

    `SECRET_KEY=<your_secret_key>
    REDIS_HOST=localhost
    REDIS_PORT=6379`

5.  **Start Redis Server**

    If you haven't installed Redis yet, install it and run the Redis server.

    bash

    Copy code

    `# On MacOS (Homebrew)
    brew install redis
    brew services start redis

    # On Linux
    sudo apt-get install redis-server
    sudo service redis-server start

    # On Windows, use WSL or Redis for Windows binaries.`

6.  **Run the Flask Application**

    bash

    Copy code

    `export FLASK_APP=app.py
    flask run`

    Your API will now be running at `http://127.0.0.1:5000`.

API Routes
----------

### 1\. **User Registration**

**Endpoint**: `/register`

**Method**: `POST`

**Request Body**:

json

Copy code

`{
  "name": "John Doe",
  "username": "johndoe",
  "password": "your_password"
}`

**Response**:

-   Success: 201 Created
-   Failure: 400 Bad Request (Invalid input)

* * * * *

### 2\. **User Login**

**Endpoint**: `/login`

**Method**: `POST`

**Request Body**:

json

Copy code

`{
  "username": "johndoe",
  "password": "your_password"
}`

**Response**:

-   Success: 200 OK with JWT token
-   Failure: 401 Unauthorized

* * * * *

### 3\. **Get Movie List**

**Endpoint**: `/movies`

**Method**: `GET`

**Description**: Returns a paginated list of movies, optionally filtered by "seen", "not_seen", or "new" status.

**Query Parameters**:

-   `page`: The page number (default: 1)
-   `page_size`: Number of movies per page (default: 10)
-   `status`: Filter by movie status: `seen`, `not_seen`, `new`

**Response**:

json

Copy code

`{
  "movies": [
    {
      "id": "movie:finch",
      "title": "Finch",
      "description": "On a post-apocalyptic Earth...",
      "release_year": 2021,
      "genres": ["Drama", "Sci-Fi"],
      "actors": ["Tom Hanks", "Caleb Landry Jones"]
    }
  ],
  "page": 1,
  "page_size": 10,
  "total_movies": 100,
  "total_pages": 10
}`

-   Success: 200 OK

* * * * *

### 4\. **Movie Action: Watched/Rating**

**Endpoint**: `/movies/action`

**Method**: `POST`

**Description**: Updates the status (watched/not watched) and/or rating of a movie.

**Request Body**:

json

Copy code

`{
  "movie_id": "movie:finch",
  "watched": true,
  "rating": 5
}`

**Response**:

-   Success: 200 OK
-   Failure: 400 Bad Request (if invalid input)

* * * * *

### 5\. **Get Movie Recommendations**

**Endpoint**: `/movies/recommendations`

**Method**: `GET`

**Description**: Returns a list of recommended movies based on user preferences.

**Query Parameters**:

-   `genres`: Comma-separated list of genres (optional)
-   `min_year`: Minimum release year (optional)
-   `max_year`: Maximum release year (optional)

**Response**:

json

Copy code

`[
  {
    "title": "Arrival",
    "release_year": 2016,
    "genres": ["Drama", "Sci-Fi"],
    "vector_distance": 0.2
  }
]`

-   Success: 200 OK
-   Failure: 404 Not Found (if user profile not found)

* * * * *

### 6\. **Similar Users**

**Endpoint**: `/similar-users`

**Method**: `GET`

**Description**: Get a list of users who have similar movie preferences.

**Response**:

json

Copy code

`[
  {
    "id": "profile:tara",
    "ratings": {
      "movie:finch": 5
    },
    "vector_distance": "0.056"
  }
]`

-   Success: 200 OK

* * * * *

### 7\. **Load Movie Data**

**Endpoint**: `/load-movies`

**Method**: `GET`

**Description**: Loads movie data from a JSON file (`data/cleaned_movies_data.json`) and inserts it into Redis.

**Response**:

-   Success: 200 OK
-   Failure: 500 Internal Server Error (if an error occurs)

Environment Variables
---------------------

Create a `.env` file in the root of your project and add the following variables:

bash

Copy code

`SECRET_KEY=<your_secret_key>
REDIS_HOST=localhost
REDIS_PORT=6379`

Running the Application
-----------------------

1.  Install the dependencies using:

    bash

    Copy code

    `pip install -r requirements.txt`

2.  Run the Flask app:

    bash

    Copy code

    `export FLASK_APP=app.py
    flask run`

    This will start the app at `http://127.0.0.1:5000`.

Movie Data
----------

The movie data is loaded into Redis from a JSON file (`data/cleaned_movies_data.json`). You can use the `/load-movies` route to load the data.
