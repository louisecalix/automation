import pandas as pd
from plyer import notification

def find_highest_rating(csv_file):
    df = pd.read_csv(csv_file)
    
    if 'Average Rating' in df.columns:
        df = df.dropna(subset=['Average Rating'])
        
        df['Average Rating'] = pd.to_numeric(df['Average Rating'], errors='coerce') 
        df = df.dropna(subset=['Average Rating'])
        
        if not df.empty:
            highest_avg_rating = df['Average Rating'].max()  # find row with highest average rating
            highest_rated_movies = df[df['Average Rating'] == highest_avg_rating]
            
            movie_platforms = {}  # collect all platforms available
            for _, row in highest_rated_movies.iterrows():
                title = row['Title']
                platform = row['Platform']
                if title not in movie_platforms:
                    movie_platforms[title] = []
                movie_platforms[title].append(platform)
            
            result = []
            for title, platforms in movie_platforms.items():
                result.append({
                    'Title': title,
                    'Average Rating': highest_avg_rating,
                    'Platforms': ', '.join(platforms)
                })
            
            return result

def send_notification(movie):
    title = movie['Title']
    average_rating = movie['Average Rating']
    platforms = movie['Platforms']
    
    notification.notify(
        title="Highest Rated Movie",
        message=f"Title: {title}\nAverage Rating: {average_rating}%\nPlatforms: {platforms}",
        timeout=100  # how long mag stay sa screen
    )


def run():
    csv_file = 'movie_data.csv'
    highest_movies = find_highest_rating(csv_file)
    if highest_movies:
        for movie in highest_movies:
            # print("Highest Rated Movie")
            # print(f"Title: {movie['Title']}")
            # print(f"Average Rating: {movie['Average Rating']}%")
            # print(f"Platforms: {movie['Platforms']}")
            # print()
            
            send_notification(movie)
