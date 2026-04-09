from aiogram.fsm.state import StatesGroup, State

class FindMovieState(StatesGroup):
    waiting_for_name = State()