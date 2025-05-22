from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNELS_URL

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧠 ChatGPT")],
        [KeyboardButton(text="🔎 Wikipedia"), KeyboardButton(text="🌦️ Ob-havo")],
        [KeyboardButton(text="💸 Valyuta"), KeyboardButton(text="🌍 Tarjima")],
        [KeyboardButton(text="🔙 Orqaga")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Bo'limni tanlang..."
)

location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text="📍 Lokatsiya jo'natish", request_location=True)],
    [KeyboardButton(text="🔙 Orqaga")]
])

channels_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 1-kanalga obuna bo'lish", url=CHANNELS_URL[0])],
    [InlineKeyboardButton(text="📢 2-kanalga obuna bo'lish", url=CHANNELS_URL[1])],
    [InlineKeyboardButton(text="📢 3-kanalga obuna bo'lish", url=CHANNELS_URL[2])],
])

wikipedia_lang_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton(text="🇺🇿 O'zbekcha"), KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇸 English")],
    [KeyboardButton(text="🔙 Orqaga")],
])

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

translation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 ▶️ 🇷🇺", callback_data='uz_ru'),
            InlineKeyboardButton(text="🇷🇺 ▶️ 🇺🇿", callback_data='ru_uz')
        ],
        [
            InlineKeyboardButton(text="🇺🇸 ▶️ 🇷🇺", callback_data='en_ru'),
            InlineKeyboardButton(text="🇷🇺 ▶️ 🇺🇸", callback_data='ru_en')
        ],
        [
            InlineKeyboardButton(text="🇺🇸 ▶️ 🇺🇿", callback_data='en_uz'),
            InlineKeyboardButton(text="🇺🇿 ▶️ 🇺🇸", callback_data='uz_en')
        ],
    ]
)
