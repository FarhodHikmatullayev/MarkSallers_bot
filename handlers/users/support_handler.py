from aiogram import types

from keyboards.default.back_menu import back_menu
from loader import bot, dp


@dp.message_handler(text='Qo\'llab quvvatlash')
async def support(message: types.Message):
    text = "Bot haqida to'liq ma'lumot olish hamda talab va takliflar uchun bizga bog'laning: \n\n" \
           "Tel: +998900832345\n" \
           "Command: /help\n" \
           "Telegram: https://t.me/pydev8747\n" \
           "Pochta manzili: farhodjonhikmatullayev@gmail.com\n" \
           "\n" \
           "Yuqoridagilardan biri orqali murojaat qiling"
    await message.answer(text=text, reply_markup=back_menu)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
