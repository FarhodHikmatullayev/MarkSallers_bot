from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import menu
from loader import dp


@dp.message_handler(text='◀ Bosh Menyu', state='*')
async def back_to_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Quyidagi bo\'limlardan birini tanlang', reply_markup=menu)
    await state.finish()