import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import main_menu, location_keyboard, channels_keyboard, wikipedia_lang_keyboard, translation_keyboard
from config import BOT_TOKEN, CHANNELS_ID
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from states import ChatGPTStates, WikipediaStates, WeatherStates, CurrencyStates, TranslateStates
from functions import check_all_channel_subscription
from handlers.wikipedia import wikipediya_javob, wikipediya_til
from handlers.chatgpt import chatgpt_javob
from handlers.translate import translate_text_function, translate_text
logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# @dp.message_handler(commands=['start']) -> aiogram==2.25.1
@dp.message(CommandStart() or F.text == "🔙 Orqaga")
async def cmd_start(message: Message, bot: Bot):
    is_subscribed = await check_all_channel_subscription(bot, message.from_user.id)
    
    if not is_subscribed:
        await message.answer(
            "Assalomu alaykum! Siz kanalga obuna bo'lishingiz kerak. "
            "Iltimos, quyidagi kanallarga obuna bo'ling va keyin qaytadan yozing.",
            reply_markup=channels_keyboard
        )
    else:
        await message.answer(
            "Assalomu alaykum! Botga xush kelibsiz! "
            "Iltimos, menyudan biror bo'limni tanlang.",
            reply_markup=main_menu
        )

   
@dp.message(F.text.in_(["🧠 ChatGPT", "🔎 Wikipedia", "🌦️ Ob-havo", "💸 Valyuta", "🌍 Tarjima", "🔙 Orqaga"]))
async def handle_menu(message: Message, state: FSMContext):
    text = message.text

    if text == "🧠 ChatGPT":
        await state.set_state(ChatGPTStates.question)
        await message.answer("Savolingizni yozing:")

    elif text == "🔎 Wikipedia":
        await state.set_state(WikipediaStates.language)
        await message.answer("Wikipedia uchun til tanlang:", reply_markup=wikipedia_lang_keyboard)
    
    elif text == "🌦️ Ob-havo":
        await message.answer(text="Siz ob-havo bo'limiga kirdingiz, obhavoni bilish uchun lokatsiya jo'nating", reply_markup=location_keyboard)
    elif text == "💸 Valyuta":
        await state.set_state(CurrencyStates.valyutadan)
        await message.answer("Valyuta kodini yozing (masalan: USD, EUR):")
    elif text == "🌍 Tarjima":
        await state.set_state(TranslateStates.tildan_tilga)
        await message.answer("Qaysi tildan qaysi tilga tarjima qilish kerak:", reply_markup=translation_keyboard)
    elif text == "🔙 Orqaga":
        await state.clear()
        await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu)
    else:
        await message.answer("Iltimos, menyudagi tugmalardan birini tanlang.")

@dp.message(WikipediaStates.language)
async def wikipedia_language_handler(message: Message, state: FSMContext):
    await wikipediya_til(message, state)

@dp.message(WikipediaStates.search)
async def wikipedia_handler(message: Message, state: FSMContext):
    await wikipediya_javob(message, state)

@dp.message(ChatGPTStates.question)
async def chatgpt_handler(message: Message, state: FSMContext):
    await chatgpt_javob(message, state)
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu)


@dp.callback_query(TranslateStates.tildan_tilga)
async def tarjima_til(call: types.CallbackQuery, state: FSMContext):
    await translate_text(call, state)

@dp.message(TranslateStates.matn)
async def tarjima_matn(message: Message, state: FSMContext):
    await translate_text_function(message, state)



async def main():
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
