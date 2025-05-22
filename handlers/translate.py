import googletrans
from states import TranslateStates


async def translate_text(call, state):
    await state.update_data(tildan_tilga=call.data)
    await call.message.answer("Tarjima qilinadigan matnni kiriting:")
    await state.set_state(TranslateStates.matn)


async def translate_text_function(message, state):
    tarjimon = googletrans.Translator()
    user_text = message.text
    await state.update_data(user_text=user_text)
    data = await state.get_data()
    language = data.get('tildan_tilga')
    tildan, tilga = language.split('_')[0], language.split('_')[1]
    tarjimasi = tarjimon.translate(text=user_text, dest=tilga, src=tildan)
    await message.answer(f"Siz so'ragan matn:\n{user_text}\n\nTarjimasi:\n{tarjimasi.text}")
    await state.clear()