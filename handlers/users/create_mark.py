from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.back_menu import back_menu
from keyboards.inline.categories import categories_keyboard, categories_callback_data
from keyboards.inline.confirmation import confirm_keyboard
from keyboards.inline.marks_keyboard import marks_keyboard, mark_callback_data
from loader import dp, db, bot
from states.marking import MarkingState


@dp.message_handler(text='Sotuvchilarga baho berish', user_id=ADMINS, state='*')
async def download_mark(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    users = await db.select_users(telegram_id=user_telegram_id)
    user = users[0]
    user_id = user['id']
    await state.finish()
    text = "Sotuvchining ID raqamini kiriting"
    await message.answer(text=text, reply_markup=back_menu)
    await MarkingState.seller_id.set()
    await state.update_data(
        {
            'user_id': user_id
        }
    )


@dp.message_handler(state=MarkingState.seller_id)
async def get_seller_id(message: types.Message, state: FSMContext):
    id = message.text
    try:
        id = int(id)
    except:
        text = "ID son bo'lishi kerak\n" \
               "Iltimos qayta urunib ko'ring"
        await message.answer(text=text, reply_markup=back_menu)
        return

    sellers = await db.select_sellers(code=id)
    if not sellers:
        text = "Bunday ID raqamli sotuvchi mavjud emas\n" \
               "Iltimos qayta urunib ko'ring"
        await message.answer(text=text, reply_markup=back_menu)
        return
    else:
        seller = sellers[0]
        seller_id = seller['id']
        await state.update_data(
            {
                'seller_id': seller_id
            }
        )
        markup = await categories_keyboard()
        await message.answer(text="Baholash kategoriyalaridan birini tanlang", reply_markup=markup)
        await MarkingState.category_id.set()


@dp.callback_query_handler(categories_callback_data.filter(), state=MarkingState.category_id)
async def get_category_id(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = int(callback_data.get('category_id'))
    await state.update_data(
        {
            'category_id': category_id
        }
    )
    category = await db.select_category(id=category_id)
    text = f"Sotuvchiga {category['title']} bo'yicha baho bering"
    await call.message.edit_text(text=text, reply_markup=marks_keyboard)
    await MarkingState.mark.set()


@dp.callback_query_handler(mark_callback_data.filter(), state=MarkingState.mark)
async def get_mark_for_seller(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    mark = callback_data.get('mark')
    await state.update_data(
        {
            'mark': mark
        }
    )
    text = "Bu ballni qo'yganingizga izoh yozing"
    await call.message.edit_text(text=text)
    await MarkingState.description.set()


@dp.callback_query_handler(text='yes', state=MarkingState.description)
async def confirm_saving_mark(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mark = await db.create_mark(
        seller_id=data.get('seller_id'),
        user_id=data.get('user_id'),
        category_id=data.get('category_id'),
        mark=int(data.get('mark')),
        description=data.get('description')
    )
    await call.message.answer(text="Muvaffaqiyatli saqlandi", reply_markup=back_menu)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(text='no', state=MarkingState.description)
async def cancel_saving_mark(call: types.CallbackQuery, state: FSMContext):
    text = "Saqlashni rad etdingiz"
    await call.message.answer(text=text, reply_markup=back_menu)
    await state.finish()


@dp.message_handler(state=MarkingState.description)
async def get_mark_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(
        {
            'description': description
        }
    )
    data = await state.get_data()
    category_id = data.get('category_id')
    category = await db.select_category(id=category_id)
    text = f"Sizning bahoyingiz quyidagicha👇\n" \
           f"Sotuvchi ID raqami: {data.get('seller_id')}\n" \
           f"Baholash kategoriyasi: {category['title']}\n" \
           f"Siz qo'ygan ball: {data.get('mark')}\n" \
           f"Izoh: {data.get('description')}\n" \
           f"\n" \
           f"Uni saqlashni istaysizmi?"
    await message.answer(text=text, reply_markup=confirm_keyboard)
