
def normalize_rating(rating, highest_rating=10):
    return (rating / highest_rating) * 100

def get_average(tmdb, rt):    
    try:
        tmdb = float(tmdb)
        tmdb_percent = normalize_rating(tmdb)
    except ValueError:
        tmdb_percent = None

    if rt == 'N/A':
        rt_percent = None
    else:
        try:
            rt_percent = float(rt)
        except ValueError:
            rt_percent = None

    ratings = [rating for rating in [tmdb_percent, rt_percent] if rating is not None]
    
    if not ratings:
        return 'N/A' 

    average_percentage = sum(ratings) / len(ratings)
    return f"{int(average_percentage)}"