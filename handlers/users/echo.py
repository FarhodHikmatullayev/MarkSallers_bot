from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# Echo bot
@dp.message_handler(state='*')
async def bot_echo(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(message.text)
