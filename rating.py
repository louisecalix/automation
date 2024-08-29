# def normalize_rating(rating, highest_rating=10): 
#     return (rating/highest_rating) * 100 # to get percentage over 100%

# def get_average(tmdb, rt):
#     tmdb = float(tmdb)
#     tmdb_percent = normalize_rating(tmdb)
#     rt_percent = rt # no need to normalize since its already over 100%

#     ratings = [tmdb_percent, rt_percent]
#     average_percentage = sum(ratings) / len(ratings)

#     return average_percentage
    

def normalize_rating(rating, highest_rating=10):
    """Normalize the rating to a percentage over 100%."""
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
        return 'N/A'  # return 'N/A' if no valid ratings are available

    average_percentage = sum(ratings) / len(ratings)
    return f"{int(average_percentage)}%"