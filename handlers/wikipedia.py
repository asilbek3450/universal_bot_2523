from aiogram import types
from aiogram.fsm.context import FSMContext
from states import WikipediaStates
import wikipedia

async def wikipediya_til(message: types.Message, state: FSMContext):
    til = message.text
    if til == "🇺🇿 O'zbekcha":
        til = "uz"
    elif til == "🇷🇺 Русский":
        til = "ru"
    elif til == "🇺🇸 English":
        til = "en"
    else:
        await message.answer("Iltimos, Wikipedia uchun to'g'ri tilni tanlang.")
        return
    await state.update_data(language=til)
    await message.answer("Iltimos, Wikipedia'da qidiriladigan savolni kiriting:")
    await state.set_state(WikipediaStates.search)



async def wikipediya_javob(message: types.Message, state: FSMContext):
    savol = message.text
    til = (await state.get_data()).get("language")
    wikipedia.set_lang(til)
    await message.answer("Siz so'ragan savolni qabul qildim. Javobni kuting...")
    try:
        natija = wikipedia.summary(savol)
        await message.answer(natija)
    except wikipedia.exceptions.DisambiguationError as e:
        await message.answer("Iltimos, aniqroq savol bering.")
    except wikipedia.exceptions.PageError as e:
        await message.answer("Bu sahifa topilmadi. Iltimos, boshqa so'zlar bilan qayta urinib ko'ring.")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
    finally:
        await state.clear()
        
