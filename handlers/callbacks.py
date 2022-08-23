from aiogram import types, Dispatcher
from apps.common import cb_menu


async def receive_f(call: types.CallbackQuery):
    try:
        await call.message.edit_text('Kak dela?')
        await call.answer()
    except Exception as e:
        print(e)

async def send(call: types.CallbackQuery):
    await call.message.answer('sosi huy')
    await call.answer()

def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(receive_f, cb_menu.filter(action='receive'))
    dp.register_callback_query_handler(send, cb_menu.filter(action='send'))
