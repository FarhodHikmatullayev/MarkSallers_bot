import datetime
import tempfile
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
import openpyxl
import os

from data.config import ADMINS
from keyboards.default.back_menu import back_menu
from loader import dp, db, bot


async def download_all_comments_function():
    marks = await db.select_all_marks()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    worksheet['A1'] = 'T/r'
    worksheet['B1'] = 'FULL_NAME'
    worksheet['C1'] = 'USERNAME'
    worksheet['D1'] = 'PHONE'
    worksheet['E1'] = 'TELEGRAM_ID'
    worksheet['F1'] = 'FILIAL NOMI'
    worksheet['G1'] = 'XODIM ID RAQAMI'
    worksheet['H1'] = 'BAHO'
    worksheet['I1'] = 'FIKR'
    worksheet['J1'] = 'VAQT'

    worksheet.cell(row=1, column=1, value='№')
    worksheet.cell(row=1, column=2, value='FULL_NAME')
    worksheet.cell(row=1, column=3, value="USERNAME")
    worksheet.cell(row=1, column=4, value='PHONE')
    worksheet.cell(row=1, column=5, value='TELEGRAM_ID')
    worksheet.cell(row=1, column=6, value='FILIAL NOMI')
    worksheet.cell(row=1, column=8, value='XODIM ID RAQAMI')
    worksheet.cell(row=1, column=9, value='BAHO')
    worksheet.cell(row=1, column=10, value='FIKR')
    worksheet.cell(row=1, column=11, value='VAQT')
    tr = 0
    for row, mark in enumerate(marks, start=2):
        user_id = mark['user_id']
        seller_id = mark['seller_id']
        users = await db.select_users(id=user_id)
        user = users[0]
        sellers = await db.select_sellers(id=seller_id)
        seller = sellers[0]
        seller_code = seller['code']
        branch_id = seller['branch_id']
        branch = await db.select_branch(id=branch_id)

        branch_name = branch['name']
        full_name = user['full_name']
        username = user['username']
        phone = user['phone']
        telegram_id = user['telegram_id']

        tr += 1
        worksheet.cell(row=row, column=1, value=tr)
        worksheet.cell(row=row, column=2, value=full_name)
        worksheet.cell(row=row, column=3, value=username)
        worksheet.cell(row=row, column=4, value=phone)
        worksheet.cell(row=row, column=5, value=telegram_id)
        worksheet.cell(row=row, column=6, value=branch_name)
        worksheet.cell(row=row, column=7, value=seller_code)
        worksheet.cell(row=row, column=8, value=mark['mark'])
        worksheet.cell(row=row, column=9, value=mark['description'])
        worksheet.cell(row=row, column=10,
                       value=mark['created_at'].strftime('%Y-%m-%d %H:%M:%S'))

    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, 'Comments_data.xlsx')
    workbook.save(file_path)

    return temp_dir


@dp.message_handler(text='Bildirilgan baholarni yuklab olish', user_id=ADMINS, state='*')
async def download_mark(message: Message, state: FSMContext):
    await state.finish()
    temp_dir = await download_all_comments_function()

    with open(os.path.join(temp_dir, 'Comments_data.xlsx'), 'rb') as file:
        await message.answer_document(document=file)
        # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    os.remove(os.path.join(temp_dir, 'Comments_data.xlsx'))


@dp.message_handler(text="Bildirilgan baholarni yuklab olish", state='*')
async def download_emp(message: Message, state: FSMContext):
    await state.finish()
    text = "Bu komanda faqat adminlar uchun"
    await message.answer(text=text, reply_markup=back_menu)
