from aiogram.fsm.state import StatesGroup, State

class ChatGPTStates(StatesGroup):
    question = State()
    answer = State()

class WikipediaStates(StatesGroup):
    search = State()

class WeatherStates(StatesGroup):
    ask_city = State()

class CurrencyStates(StatesGroup):
    ask_currency = State()

class TranslateStates(StatesGroup):
    ask_text = State()
