import requests
import csv
import sys

# API routes and auth
discover_url_template = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={}&sort_by=popularity.desc"
similar_url_template = "https://api.themoviedb.org/3/movie/{}/similar?language=en-US&page={}"
auth_header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlODA1NWViZjE2YjAxYTNlOWY5OGJlNzlmOGEyMzI2NyIsInN1YiI6IjY1MzE5MzBiNmY4ZDk1MDEyY2QwOTFmNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.btnceJg5kvnZ1pPyj-7TbSs2Ia4qCzc9wdGGtdTutOo"
}

# Function that gets all the movies from a given page (these movies to be used as the keys of the graph)
def fetch_movies(url_template, page):
    response = requests.get(url_template.format(page), headers=auth_header)
    if response.status_code == 200:
        return [(movie['id'], movie['title']) for movie in response.json().get('results', [])]
    # If the status code is 429, the program will terminate because that means the rate limit has been exceeded for TMDB
    elif response.status_code == 429:
        print("Rate limit exceeded. Terminating the program.")
        sys.exit(1)
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return []

# Function to get similar movies based on the keys of the graph
def fetch_similar_movies(movie_id):
    similar_movies = []
    for page in range(1, 3):  # calls route twice which is 40 similar movies per key
        similar = fetch_movies(similar_url_template.format(movie_id, page), 1)
        if similar:
            similar_movies.extend(similar)
    return similar_movies

# Calling both routes together
total_pages = 100  # used these two variables to call this program in chunks
start_page = 401 # so that I could restart the program if it failed and not lose all the data
movies_data = []
print("starting")
for page in range(start_page, start_page + total_pages):
    # Print statement to keep track of progress
    if (page % 10 == 0):
        print(f"Fetching page {page}")
    #first get the keys then get the corresponding similar movies
    movies = fetch_movies(discover_url_template, page)
    if movies:
        for movie_id, movie_title in movies:
            similar_movies = fetch_similar_movies(movie_id)
            # for each similar movie pulling the id and the title
            row = [movie_id, movie_title] + [item for sublist in similar_movies for item in sublist]
            movies_data.append(row)

# Writing movie IDs, titles, and similar movie info to csv file
csv_file = 'movies_with_similar.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(movies_data)
