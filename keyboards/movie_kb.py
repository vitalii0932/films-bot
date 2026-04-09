from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

movie_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐ Додати в обране", callback_data="add_fav"),
            InlineKeyboardButton(text="👍 Оцінити", callback_data="rate"),
        ],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ]
)