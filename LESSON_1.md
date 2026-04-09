# 📚 Урок: Telegram-бот для фільмів (Aiogram) — покрокова реалізація

## ⏱ Тривалість: ~1 год 20 хв

---

# 🎯 Мета уроку

На цьому уроці учні:

* створять Telegram-бота
* розберуть структуру проєкту
* навчаться працювати з FSM
* реалізують:
  * пошук фільму
  * обране
  * оцінки
  * inline кнопки
* зрозуміють, як працює in-memory storage

---

# 📁 КРОК 1 — Структура проєкту

Створюємо структуру:

```
bot/
 ├── handlers/
 ├── keyboards/
 ├── services/
 ├── states/
 ├── config.py
 ├── main.py
 └── .env
```

📌 Пояснення:

* `handlers` — логіка бота (що відбувається при діях)
* `keyboards` — кнопки
* `services` — робота з даними
* `states` — FSM (стани)
* `config` — конфігурація
* `main` — точка входу

---

# 🔐 КРОК 2 — Налаштування токена

## `.env`

```
TOKEN=your_token_here
```

📌 Пояснення:

* токен — це ключ доступу до бота
* його не можна пушити в Git

---

## `config.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
```

📌 Пояснення:

* `load_dotenv()` — завантажує змінні з `.env`
* `os.getenv()` — отримує значення

---

# 🚀 КРОК 3 — Запуск бота

## `main.py`

```python
import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers.user import router
from aiogram.fsm.storage.memory import MemoryStorage
```

📌 Пояснення:

* `Bot` — об'єкт бота
* `Dispatcher` — маршрутизатор подій
* `MemoryStorage` — сховище для FSM

---

```python
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await dp.start_polling(bot)
```

📌 Пояснення:

* створюємо бота
* підключаємо FSM storage
* підключаємо router
* запускаємо polling

---

```python
if __name__ == '__main__':
    asyncio.run(main())
```

📌 Пояснення:

* запуск асинхронної функції

---

# 🧠 КРОК 4 — Стани (FSM)

## `states/movie.py`

```python
from aiogram.fsm.state import StatesGroup, State

class MovieState(StatesGroup):
    waiting_for_movie = State()
```

## `states/rating.py`

```python
from aiogram.fsm.state import StatesGroup, State

class RatingState(StatesGroup):
    waiting_for_rating = State()
```

📌 Пояснення:

* `StatesGroup` — група станів
* `State()` — конкретний стан
* FSM дозволяє контролювати діалог

---

# 💾 КРОК 5 — In-memory storage

## `services/storage.py`

```python
favorites = {}
ratings = {}
current_movies = {}
```

📌 Пояснення:

* dict зберігають дані
* ключ = user_id

---

## Функції

### Додати в обране

```python
def add_to_favorites(user_id, movie):
    if user_id not in favorites:
        favorites[user_id] = []

    if movie not in favorites[user_id]:
        favorites[user_id].append(movie)
```

📌 Пояснення:

* створюємо список, якщо нема
* не допускаємо дублікати

---

### Отримати обране

```python
def get_favorites(user_id):
    return favorites.get(user_id, [])
```

---

### Оцінки

```python
def add_rating(user_id, movie, rating):
    if user_id not in ratings:
        ratings[user_id] = {}

    ratings[user_id][movie] = rating
```

---

### Поточний фільм

```python
def set_current_movie(user_id, movie):
    current_movies[user_id] = movie

def get_current_movie(user_id):
    return current_movies.get(user_id)
```

📌 Пояснення:

* кожен користувач має свій "поточний фільм"

---

# 🎮 КРОК 6 — Клавіатури

## Головна клавіатура

```python
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎬 Знайти фільм")],
        [KeyboardButton(text="⭐ Обране"), KeyboardButton(text="📊 Мої оцінки")]
    ],
    resize_keyboard=True
)
```

📌 Пояснення:

* звичайні кнопки під полем вводу

---

## Inline клавіатура

```python
def movie_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Додати в обране", callback_data="add_fav"),
                InlineKeyboardButton(text="👍 Оцінити", callback_data="rate"),
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
        ]
    )
```

📌 Пояснення:

* inline кнопки прив’язані до повідомлення
* `callback_data` — що відправляється боту

---

# 🤖 КРОК 7 — Handlers

## Router

```python
router = Router()
```

📌 Пояснення:

* збирає всі обробники

---

## /start

```python
@router.message(Command("start"))
async def start_handler(message: types.Message):
```

📌 Пояснення:

* реагує на команду `/start`

---

## Пошук фільму (FSM старт)

```python
@router.message(F.text == "🎬 Знайти фільм")
async def find_movie(message: types.Message, state: FSMContext):
```

📌 Пояснення:

* `F.text` — фільтр по тексту
* `state` — FSM контекст

---

```python
await state.set_state(MovieState.waiting_for_movie)
```

📌 Пояснення:

* переводимо користувача в стан

---

## Обробка введення

```python
@router.message(MovieState.waiting_for_movie)
```

📌 Пояснення:

* спрацьовує тільки в цьому стані

---

```python
movie = message.text.title()
```

📌 Пояснення:

* робимо гарний формат тексту

---

```python
set_current_movie(message.from_user.id, movie)
```

📌 Пояснення:

* зберігаємо фільм для користувача

---

## Inline кнопки

```python
@router.callback_query(F.data == "add_fav")
```

📌 Пояснення:

* обробка натискання кнопки

---

```python
callback.from_user.id
```

📌 Пояснення:

* отримуємо користувача

---

```python
await callback.answer()
```

📌 ВАЖЛИВО:

* обов’язково викликати
* інакше буде "loading"

---

## Оцінка

```python
await state.set_state(RatingState.waiting_for_rating)
```

📌 Пояснення:

* запускаємо FSM для оцінки

---

```python
@router.message(RatingState.waiting_for_rating)
```

📌 Пояснення:

* ловимо тільки оцінку

---

```python
if not message.text.isdigit():
```

📌 Пояснення:

* перевірка що це число

---

```python
if 1 <= rating <= 10:
```

📌 Пояснення:

* валідація

---

```python
await state.clear()
```

📌 Пояснення:

* вихід зі стану

---

## Назад

```python
@router.callback_query(F.data == "back")
```

📌 Пояснення:

* очищаємо поточний фільм

---

# ⚠️ Важливі моменти

* FSM потрібен для контролю діалогу
* storage — для збереження даних
* inline кнопки — для дій з конкретним об’єктом
* user_id — ключ до всіх даних

---

# 🏠 Домашнє завдання

1. Розробити зовнішній інтерфейс вашого боту з моками (емуляцією роботи) — як виглядатиме, які кнопки будуть, які повідомлення відправлятися
   - це допоможе зрозуміти, як користувач буде взаємодіяти з ботом
   - будувати одразу правильну структуру проєкту
   - визначити, які дані потрібно зберігати в storage
   - визначити, які стани потрібні для FSM
   - визначити, які клавіатури потрібні
   - визначити, які обробники потрібні
2. Реалізувати бота з мінімальною логікою (без API, з моками) — щоб відпрацювати структуру та FSM
   - це допоможе закріпити знання про структуру проєкту та FSM
   - зрозуміти, як працюють обробники та клавіатури
   - підготувати базу для подальшої реалізації з API

---

# 🚀 Далі

Наступний крок:

* підключення API фільмів
* реальний пошук
* постери

---