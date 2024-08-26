from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

categories_callback_data = CallbackData('category', 'category_id')


async def categories_keyboard():
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    categories = await db.select_all_categories()

    for category in categories:
        text_button = f"{category['title']}"
        callback_data = categories_callback_data.new(category_id=category['id'])
        markup.insert(
            InlineKeyboardButton(
                text=text_button,
                callback_data=callback_data,
            )
        )

    return markup
