from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.main_kb import main_keyboard
from keyboards.movie_kb import movie_keyboard
from keyboards.movies_list_kb import movies_list_keyboard
from keyboards.saved_movies_list_keyboard import saved_movies_list_keyboard
from states.find_movie_state import FindMovieState
from states.rate_movie_state import RatingState
from services.db import (
    add_to_favorites,
    get_favorites,
    add_rating,
    get_ratings,
    set_current_movie,
    get_current_movie
)
from services.tmdb import (
    search_movie,
    form_poster_url,
    get_movie_details,
    get_movie_trailer_url
)

router = Router()

@router.message(Command('start'))
async def start(message: types.Message):
    """Start command handler.

    Args:
        message (types.Message): Message object.
    """
    await message.answer(
        '👋 Привіт! Я бот для фільмів 🎬',
        reply_markup=main_keyboard
    )

@router.message(F.text == '🎬 Знайти фільм')
async def find_movie(message: types.Message, state: FSMContext):
    """Find movie btn handler

    Args:
        message (types.Message): Message object.
        state (FSMContext): FSMContext object.
    """
    await state.set_state(FindMovieState.waiting_for_name)

    await message.answer('Введіть назву фільму 🎥')

@router.message(FindMovieState.waiting_for_name)
async def process_movie_search(message: types.Message, state: FSMContext):
    """Process movie search state handler

    Args:
        message (types.Message): Message object.
        state (FSMContext): FSMContext object.
    """
    movie = message.text.title()

    movies = await search_movie(movie)

    if not movies:
        await message.answer(
            f'Нічого не знайдено по вашому запиту: {movie} 😢',
            reply_markup=main_keyboard
        )

    await message.answer(
        'Оберіть фільм 🎬',
        reply_markup=movies_list_keyboard(movies)
    )
    
    await state.clear()

@router.callback_query(F.data.startswith('select_movie:'))
async def select_movie(callback: CallbackQuery):
    """Select movie handler

    Args:
        callback (CallbackQuery): CallbackQuery object.
    """
    movie_id = callback.data.split(':')[1]

    movie = await get_movie_details(movie_id)

    title = movie['title']
    overview = movie['overview']
    rating = movie['vote_average']
    poster_path = movie['poster_path']
    poster_url = form_poster_url(poster_path)
    trailer_url = get_movie_trailer_url(movie_id)

    movie_data = {
        'id': movie_id,
        'title': title,
        'year': movie['release_date']
    }
    set_current_movie(callback.from_user.id, movie_data)

    await callback.message.answer_photo(
        photo=poster_url,
        caption=
        f'🎥 {title}\n'
        f'⭐ {rating}\n'
        f'{overview}\n\n'
        f'[🎬 Дивитись на IMDb]({trailer_url})',
        parse_mode='Markdown',
        reply_markup=movie_keyboard
    )

    await callback.answer()

@router.callback_query(F.data == 'add_fav')
async def add_fav(callback: CallbackQuery):
    movie = get_current_movie(callback.from_user.id)

    if not movie:
        await callback.answer('Спочатку оберіть фільм ❗', show_alert=True)
        return

    add_to_favorites(callback.from_user.id, movie)

    await callback.answer('Додано в обране ⭐')

@router.callback_query(F.data == 'rate')
async def rate(callback: CallbackQuery, state: FSMContext):
    movie = get_current_movie(callback.from_user.id)

    if not movie:
        await callback.answer('Спочатку оберіть фільм ❗', show_alert=True)
        return

    await state.set_state(RatingState.waiting_for_rating)
    await callback.message.answer('Введіть вашу оцінку (1-10) 👍')

    await callback.answer()

@router.message(RatingState.waiting_for_rating)
async def handle_rating(message: types.Message, state: FSMContext):
    movie = get_current_movie(message.from_user.id)

    if not movie:
        await message.answer('Спочатку оберіть фільм ❗', show_alert=True)
        await state.clear()
        return

    if not message.text.isdigit():
        await message.answer('Введіть число від 1 до 10')
        return

    rating = int(message.text)

    if not 1 <= rating <= 10:
        await message.answer('Будь-ласка, в межах від 1 до 10 😟')
        return

    add_rating(message.from_user.id, movie, rating)
    await message.answer(f"Оцінка для {movie['title']} збережена ✅")
    await state.clear()

@router.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery):
    set_current_movie(callback.from_user.id, None)
    await callback.message.answer("Обраний фільм очищено 🧹", reply_markup=main_keyboard)
    await callback.answer()

@router.message(F.text == "⭐ Обране")
async def show_fav(message: types.Message):
    favs = get_favorites(message.from_user.id)

    if not favs:
        await message.answer(
            "Список порожній 😢",
            reply_markup=main_keyboard
        )
        return

    text = "⭐ Обране:\n"

    await message.answer(
        text,
        reply_markup=saved_movies_list_keyboard(favs)
    )

@router.message(F.text == "📊 Мої оцінки")
async def show_ratings(message: types.Message):
    user_ratings = get_ratings(message.from_user.id)

    if not user_ratings:
        await message.answer(
            "Немає оцінок 😢",
            reply_markup=main_keyboard
        )
        return

    text = "📊 Ваші оцінки:\n"

    await message.answer(
        text,
        reply_markup=saved_movies_list_keyboard(user_ratings)
    )