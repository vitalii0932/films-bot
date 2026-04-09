from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🎬 Знайти фільм')],
        [KeyboardButton(text='⭐ Обране'), KeyboardButton(text='📊 Мої оцінки')],
    ], resize_keyboard=True
)