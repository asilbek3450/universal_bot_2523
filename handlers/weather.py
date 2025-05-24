from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import requests
from config import WEATHER_API_KEY
from states import WeatherStates


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        desc = data["weather"][0]["description"]

        return (
            f"🌆 Shahar: {name}\n"
            f"🌡 Harorat: {temp}°C\n"
            f"🤒 Seziladigan harorat: {feels_like}°C\n"
            f"💧 Namlik: {humidity}%\n"
            f"💨 Shamol: {wind_speed} m/s\n"
            f"🌤 Ob-havo: {desc.capitalize()}"
        )

async def obhavo_javob(message: Message, state: FSMContext):
    city = message.text.strip()
    javob = get_weather(city)

    if javob:
        await message.answer(javob)
    else:
        await message.answer("❌ Shahar topilmadi. Iltimos, qayta urinib ko‘ring.")

    await state.clear()
