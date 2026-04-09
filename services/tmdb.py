import aiohttp
from config import TMDB_API_KEY

BASE_URL = 'https://api.themoviedb.org'
BASE_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'
BASE_TRAILER_URL = 'https://www.themoviedb.org/movie'

async def search_movie(query):
    url = f'{BASE_URL}/3/search/movie'

    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'uk-UA'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            data = await resp.json()
            return data.get('results', [])

def form_poster_url(poster_path):
    return f'{BASE_IMAGE_URL}/{poster_path}'

async def get_movie_details(movie_id):
    url = f'{BASE_URL}/3/movie/{movie_id}'

    params = {
        'api_key': TMDB_API_KEY,
        'language': 'uk-UA'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

def get_movie_trailer_url(movie_id):
    return f'{BASE_TRAILER_URL}/{movie_id}/videos'