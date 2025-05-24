import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import main_menu, location_keyboard, channels_keyboard, wikipedia_lang_keyboard, from_lang_keyboard, from_to_currency_keyboard
from config import BOT_TOKEN, CHANNELS_ID
from aiogram.fsm.context import FSMContext
from states import ChatGPTStates, WikipediaStates, WeatherStates, CurrencyStates, TranslateStates
from functions import check_all_channel_subscription
from handlers.wikipedia import wikipediya_javob, wikipediya_til
from handlers.chatgpt import chatgpt_javob
from handlers.translate import translator_tildan, translator_tilga, matn_tarjima   
from handlers.weather import obhavo_javob
from handlers.valyuta import process_currency_conversion
from aiogram.types import ReplyKeyboardRemove
from states import CurrencyStates
logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

    elif text == "🌍 Tarjima":
        await state.set_state(TranslateStates.qaysi_tildan)
        await message.answer("Qaysi tildan tarjima qilish kerak:", reply_markup=from_lang_keyboard)
    

    elif text == "🌦️ Ob-havo":
        await state.set_state(WeatherStates.ask_city)       
        await message.answer(text="Ob-havoni bilish uchun shaharni jo'nating")
    
    
    elif text == "💸 Valyuta":
        await state.set_state(CurrencyStates.valyutadan)
        await message.answer("Valyuta kodini yozing :" , reply_markup=from_to_currency_keyboard)
   
   
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



@dp.message(TranslateStates.qaysi_tildan)
async def translator_tildan_handler(message: Message, state: FSMContext):
    await translator_tildan(message, state)

@dp.message(TranslateStates.qaysi_tilga)
async def translator_tilga_handler(message: Message, state: FSMContext):
    await translator_tilga(message, state)

@dp.message(TranslateStates.matn)
async def matn_tarjima_handler(message: Message, state: FSMContext):
    await matn_tarjima(message, state)
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu)



@dp.message(WeatherStates.ask_city)
async def weather_city_handler(message: Message, state: FSMContext):
    await obhavo_javob(message, state)
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu)




@dp.message(CurrencyStates.valyutadan)
async def from_currency_chosen(message: Message, state: FSMContext):
    from_ccy = message.text.strip().upper()
    await state.update_data(from_ccy=from_ccy)
    await message.answer("Qaysi valyutaga o‘girmoqchisiz?", reply_markup=from_to_currency_keyboard)
    await state.set_state(CurrencyStates.valyutaga)



@dp.message(CurrencyStates.valyutaga)
async def to_currency_chosen(message: Message, state: FSMContext):
    to_ccy = message.text.strip().upper()
    await state.update_data(to_ccy=to_ccy)
    await message.answer("O‘girmoqchi bo‘lgan miqdorni kiriting (faqat son):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CurrencyStates.qancha)



@dp.message(CurrencyStates.qancha)
async def amount_entered_handler(message: Message, state: FSMContext):
    await process_currency_conversion(message, state)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

