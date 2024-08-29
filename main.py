import requests
from datetime import datetime
import csv
import random
import scrape
import notification

# Read the API key from a file
with open('api_key/key.txt', "r") as file:
    api_key = file.read().strip()

# Define genre codes for TMDb
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

def fetch_movies_by_genre(genre_id, genre_name):  # Function to get movie title
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies = response.json()
        count = 0
        movie_details = []
        for movie in movies['results']:
            if count >= 1:  # Fetch only one movie per genre
                break
            release_year = datetime.strptime(movie['release_date'], '%Y-%m-%d').year  # Extract release year
            tmdb_rating = movie.get('vote_average', 'N/A')  # Get TMDb rating
            try:
                tmdb_rating = float(tmdb_rating)
            except ValueError:
                tmdb_rating = 'N/A'
            
            # Fetch where to watch information (replace with your actual implementation)
            platforms = scrape.fetch_where_to_watch(movie['title'], release_year, genre_name, tmdb_rating)
            
            movie_details.append({
                'Title': movie['title'],
                'Year': release_year,
                'Genre': genre_name,
                'TMDB Rating': tmdb_rating,
                'RT Rating': 'N/A',  # Placeholder for Rotten Tomatoes rating
                'Average Rating': 'N/A',  # Placeholder for Average Rating
                'Platform': platforms,
                'URL': movie.get('homepage', 'N/A')  # Get movie URL if available
            })
            count += 1

        return movie_details

if __name__ == '__main__':
    # File to save movie data
    csv_file = 'movie_data.csv'

    # Write header to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Year', 'Genre', 'TMDB Rating', 'RT Rating', 'Average Rating', 'Platform', 'URL'])
        writer.writeheader()

    # Generate 5 random genres
    random_genres = random.sample(list(genres.items()), 5)

    all_movie_details = []

    # Fetch movies for each random genre
    for genre_name, genre_id in random_genres:
        print(f"\nFetching movies for genre: {genre_name}")
        movie_details = fetch_movies_by_genre(genre_id, genre_name)
        all_movie_details.extend(movie_details)
        
    # Write movie data to CSV file
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Year', 'Genre', 'TMDB Rating', 'RT Rating', 'Average Rating', 'Platform', 'URL'])
        writer.writerows(all_movie_details)

    # Run notifications
    notification.run()
