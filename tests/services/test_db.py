import pytest
from services import db

@pytest.fixture(autouse=True)
def clear_db():
    db.favorites.clear()
    db.ratings.clear()
    db.current_movies.clear()

def test_add_to_favorite():
    user_id = 'test'
    movie = {'id': 1, 'title': 'Test', 'year': 1999}

    db.add_to_favorites(user_id, movie)

    assert len(db.favorites[user_id]) == 1
    assert db.favorites[user_id][0] == movie

def test_add_to_favorite_duplicate():
    user_id = 'test'
    movie = {'id': 1, 'title': 'Test', 'year': 1999}

    db.add_to_favorites(user_id, movie)
    db.add_to_favorites(user_id, movie)

    assert len(db.favorites[user_id]) == 1
    assert db.favorites[user_id][0] == movie

def test_add_rating():
    user_id = 'test'
    movie = {'id': 1, 'title': 'Test', 'year': 1999}
    rating = 9

    db.add_rating(user_id, movie, rating)

    assert len(db.ratings[user_id]) == 1
    assert db.ratings[user_id][0]['id'] == movie['id']
    assert db.ratings[user_id][0]['title'] == movie['title']
    assert db.ratings[user_id][0]['year'] == movie['year']
    assert db.ratings[user_id][0]['rating'] == rating

def test_change_rating():
    user_id = 1
    movie = {'id': 1, 'title': 'Test', 'year': 1999}
    rating = 9

    db.add_rating(user_id, movie, rating)
    rating = 10
    db.add_rating(user_id, movie, rating)

    assert len(db.ratings[user_id]) == 1
    assert db.ratings[user_id][0]['id'] == movie['id']
    assert db.ratings[user_id][0]['title'] == movie['title']
    assert db.ratings[user_id][0]['year'] == movie['year']
    assert db.ratings[user_id][0]['rating'] == rating