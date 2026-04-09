favorites = {} # { user_id: [movie_dict] }
ratings = {} # { user_id: [movie_dict + rating] }
current_movies = {} # { user_id: movie_dict }

def add_to_favorites(user_id, movie: dict):
    if user_id not in favorites:
        favorites[user_id] = []

    if not any(m['id'] == movie['id'] for m in favorites[user_id]):
        favorites[user_id].append(movie)

def get_favorites(user_id):
    return favorites.get(user_id, [])

def add_rating(user_id, movie: dict, rating):
    movie_copy = movie.copy()

    if user_id not in ratings:
        ratings[user_id] = []

    for m in ratings[user_id]:
        if m['id'] == movie_copy['id']:
            m['rating'] = rating
            return

    movie_copy['rating'] = rating
    ratings[user_id].append(movie_copy)

def get_ratings(user_id):
    return ratings.get(user_id, {})

def set_current_movie(user_id, movie: dict):
    current_movies[user_id] = movie

def get_current_movie(user_id):
    return current_movies.get(user_id)