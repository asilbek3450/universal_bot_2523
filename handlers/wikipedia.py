from aiogram import types
from aiogram.fsm.context import FSMContext
import wikipedia


async def wikipediya_javob(message: types.Message, state: FSMContext):
    savol = message.text
    await message.answer("Siz so'ragan savolni qabul qildim. Javobni kuting...")
    wikipedia.set_lang("uz")
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
        
