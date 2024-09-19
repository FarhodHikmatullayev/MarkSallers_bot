from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.main_menu import menu
from loader import dp


# Echo bot
@dp.message_handler(state='*')
async def bot_echo(message: types.Message, state: FSMContext):

    if str(message.from_user.id) in ADMINS:
        menu_keyboard = await menu(is_admin=True)
    else:
        menu_keyboard = await menu()

    await state.finish()
    text = "Bunday buyruq mavjud emas!"
    await message.answer(text)
    text = "Botdan foydalanish uchun quyidagi bo'limlardan birini tanlang"
    await message.answer(text=text, reply_markup=menu_keyboard)