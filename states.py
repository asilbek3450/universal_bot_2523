from aiogram.fsm.state import StatesGroup, State

class ChatGPTStates(StatesGroup):
    question = State()
    answer = State()

class WikipediaStates(StatesGroup):
    language = State()
    search = State()

class WeatherStates(StatesGroup):
    ask_city = State()

class CurrencyStates(StatesGroup):
    valyutadan = State()
    valyutaga = State()
    qancha = State()

class TranslateStates(StatesGroup):
    tildan_tilga = State()
    matn = State()
    
