from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def saved_movies_list_keyboard(movies):
    keyboard = []

    for movie in movies:
        id = movie['id']
        title = movie['title']
        year = movie['year']
        rating = movie.get('rating')

        if rating:
            keyboard.append([InlineKeyboardButton(
                text=f"{title} - {year}: {rating} / 10 ⭐",
                callback_data=f'select_movie:{id}'
            )])
        else:
            keyboard.append([InlineKeyboardButton(
                text=f'{title} - {year}',
                callback_data=f'select_movie:{id}'
            )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)