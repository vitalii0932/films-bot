from aiogram.fsm.state import StatesGroup, State

class RatingState(StatesGroup):
    waiting_for_rating = State()