from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def chatgpt_question(message: Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await message.answer("Savolingizni qabul qildim. Javobni kuting...")
    # Here you would typically call the ChatGPT API and send the response back to the user.
    # For now, we will just simulate a response.
    await message.answer("Bu yerda ChatGPT javobi bo'ladi.")
    await state.clear()
    