from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def menu(is_admin=False):
    if is_admin:
        return menu_for_admins
    else:
        return basic_menu


menu_for_admins = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Sotuvchilarga baho berish"),
        ],
        [
            KeyboardButton(text="Qo'llab quvvatlash"),
        ],
        [
            KeyboardButton(text="Bildirilgan baholarni yuklab olish"),
        ],
        [
            KeyboardButton(text="Download sellers"),
            KeyboardButton(text="Upload sellers"),
        ]
    ]
)

basic_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Sotuvchilarga baho berish"),
        ],
        [
            KeyboardButton(text="Qo'llab quvvatlash"),
        ],
    ]
)
