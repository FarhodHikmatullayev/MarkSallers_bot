import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from data.config import ADMINS
from keyboards.default.main_menu import menu
from keyboards.default.contakt_button import keyboard
from loader import dp, db


@dp.message_handler(content_types='contact')
async def get_contact(message: Message):
    contact = message.contact
    if str(message.from_user.id) in ADMINS:
        menu_keyboard = await menu(is_admin=True)
    else:
        menu_keyboard = await menu()

    try:
        user = await db.create_user(phone=contact.phone_number, telegram_id=message.from_user.id,
                                    username=message.from_user.username, full_name=message.from_user.full_name)
        await message.answer(f"Rahmat, <b>{contact.full_name}</b>.\n"
                             f"Sizning {contact.phone_number} raqamingizni qabul qildik.",
                             reply_markup=ReplyKeyboardRemove())

        await message.answer(text="Endi quyidagi bo'limlardan birini tanlang", reply_markup=menu_keyboard)

    except asyncpg.exceptions.UniqueViolationError:

        text = "Siz allaqachon ro'yxatdan o'tgan ekansiz\n" \
               "Endi quyidagi bo'limlardan birini tanlang"
        await message.answer(text=text, reply_markup=menu_keyboard)


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    print('user_telegram_id', message.from_user.id)

    users = await db.select_users(telegram_id=message.from_user.id)

    if users:
        if str(message.from_user.id) in ADMINS:
            menu_keyboard = await menu(is_admin=True)
        else:
            menu_keyboard = await menu()
        await message.answer(text="Quyidagi bo'limlardan birini tanlang", reply_markup=menu_keyboard)
    else:
        text = f"Salom, {message.from_user.full_name}!\n"
        text += "Botimizga xush kelibsiz\n" \
                "Botdan ro'yxatdan o'tish uchun kontaktingizni yuboring"

        await message.answer(text, reply_markup=keyboard)
        await state.finish()
