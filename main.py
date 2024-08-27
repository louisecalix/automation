import requests
from datetime import datetime
import csv
import scrape


api_key = open('api_key/key.txt', "r")
api_key = api_key.read()

genres = {
    'Action': 28,
    'Animated': 16,
    'Documentary': 99,
    'Drama': 18,
    'Family': 10751,
    'Fantasy': 14,
    'History': 36,
    'Comedy': 35,
    'War': 10752,
    'Crime': 80,
    'Mystery': 9648,
    'Romance': 10749,
    'Sci-Fi': 878,
    'Horror': 27,
    'Thriller': 53,
    'Adventure': 12
}


def fetch_movies_by_genre(genre_id, genre_name):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies = response.json()
        count = 0
        for movie in movies['results']:
            if count >= 1:
                break
            release_year = datetime.strptime(movie['release_date'], '%Y-%m-%d').year
            rating = movie.get('vote_average', 'N/A') 
            scrape.fetch_where_to_watch(movie['title'], release_year, genre_name, rating)
            count += 1

with open('movie_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Year', 'Genre', 'Rating', 'Platform', 'URL'])

for genre_name, genre_id in genres.items():
    print(f"\nFetching movies for genre: {genre_name}")
    fetch_movies_by_genre(genre_id, genre_name)
