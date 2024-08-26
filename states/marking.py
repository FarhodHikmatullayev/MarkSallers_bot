from aiogram.dispatcher.filters.state import State, StatesGroup


class MarkingState(StatesGroup):
    seller_id = State()
    user_id = State()
    mark = State()
    description = State()
    category_id = State()
