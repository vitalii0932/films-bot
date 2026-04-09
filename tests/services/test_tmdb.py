import pytest
from services import tmdb

@pytest.mark.parametrize('poster_path, expected_url', [
    ('123.jpg', 'https://image.tmdb.org/t/p/w500/123.jpg'),
    ('345.jpg', 'https://image.tmdb.org/t/p/w500/345.jpg')
])
def test_form_poster_url(poster_path, expected_url):
    assert tmdb.form_poster_url(poster_path) == expected_url

@pytest.mark.parametrize('movie_id, expected_url', [
    ('123', 'https://www.themoviedb.org/movie/123/videos'),
    ('345', 'https://www.themoviedb.org/movie/345/videos')
])
def test_get_movie_trailer_url(movie_id, expected_url):
    assert tmdb.get_movie_trailer_url(movie_id) == expected_url