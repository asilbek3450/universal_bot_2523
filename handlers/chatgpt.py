from aiogram import types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import requests

url = "https://open-ai21.p.rapidapi.com/conversationllama"

async def chatgpt_javob(message: Message, state: FSMContext):
    question = message.text
    await state.update_data(question=question)
    await message.answer("Savolingizni qabul qildim. Javob tayyorlanmoqda...")
    payload = {
        "messages": [
            {"role": "user", "content": question}
        ],"web_access": False
    }
    headers = {
        "x-rapidapi-key": "0e1e80d5bfmsh213ed89c8e67ef5p10d6b3jsn0c4cbb51f1b1",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    answer = requests.post(url, json=payload, headers=headers).json().get('result')
    if answer:
        await message.answer(f"ChatGPT bergan javob:\n\n{answer}")
    else:
        await message.answer("Javob topilmadi. Iltimos, boshqa savol bering.")
    await state.clear()
