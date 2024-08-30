import requests
from datetime import datetime
import csv
import scrape
import notification
import random
import schedule
import time


api_key = open('api_key/key.txt', "r") # put your api key here from tmdb to get movie titles per genre
api_key = api_key.read()

# genre code for tmdb
genres = {
    'Action': 28,
    # 'Animated': 16,
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


def fetch_movies_by_genre(genre_id, genre_name): # function to get movie title by genre
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies = response.json()
        count = 0
        for movie in movies['results']:
            if count >= 1: # ilang movie per genre
                break
            release_year = datetime.strptime(movie['release_date'], '%Y-%m-%d').year # year released
            tmdb_rating = movie.get('vote_average', 'N/A') # tmdb rating
            tmdb_rating = float(tmdb_rating)
            scrape.fetch_where_to_watch(movie['title'], release_year, genre_name, tmdb_rating) # platforms available
            count += 1


def task():
    with open('movie_data.csv', 'w', newline='', encoding='utf-8') as csvfile: # write in csv file
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Year', 'Genre', 'TMDB Rating', 'RT Rating','FA Rating', 'Average Rating', 'Platform', 'URL'])

    random_genres = random.sample(list(genres.items()), 5) # to select 5 random genres

    for genre_name, genre_id in random_genres:
        print(f"\nFetching movies for genre: {genre_name} (ID: {genre_id})")
        fetch_movies_by_genre(genre_id, genre_name)

    notification.run()
    

task()

# if __name__ == '__main__':
#     # schedule.every().day.at("10:00").do(job)
#     schedule.every(5).minutes.do(task) # to run the script every 5 minutes

#     print("Scheduler started. The script will run every 5 minutes.")
    
#     while True:
#         schedule.run_pending() 
#         time.sleep(1)  