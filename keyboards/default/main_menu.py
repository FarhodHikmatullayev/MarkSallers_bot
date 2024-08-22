from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
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
