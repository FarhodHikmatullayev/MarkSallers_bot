from aiogram.dispatcher.filters.state import State, StatesGroup


class AddSellerState(StatesGroup):
    waiting_for_excel_file = State()
