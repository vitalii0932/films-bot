from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def movies_list_keyboard(movies):
    keyboard = []

    for movie in movies[:5]:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{movie['title']}: {movie['release_date']}",
                callback_data=f"select_movie:{movie['id']}"
            )
        ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)