from aiogram import types, Dispatcher

from apps.common import cb_menu, cb_wallet
from apps.database import select_address
from localization import get_string

from apps.keyboard import menu, list_of_wallets


async def receive_f(call: types.CallbackQuery):
    try:
        await call.message.edit_text('Kak dela?')
        await call.answer()
    except Exception as e:
        print(e)


async def send(call: types.CallbackQuery):
    await call.message.answer('sosi huy')
    await call.answer()


async def make_list_of_wallets_call(call: types.CallbackQuery):
    try:
        await call.message.edit_text(text=get_string(call.from_user.language_code, "wallets"),
                                     reply_markup=await list_of_wallets(call.from_user.id))
        await call.answer()
    except Exception as e:
        print(e)


async def make_wallets_menu(call: types.CallbackQuery, callback_data: dict):
    name = callback_data["name"]
    address = await select_address(call.from_user.id, name)
    text = get_string(call.from_user.language_code, 'wal_name') + f' *{name}*\n'
    text += get_string(call.from_user.language_code, 'wal_address') + f'*{address[0][0]}*'
    await call.message.edit_text(text, parse_mode="MarkdownV2", reply_markup=menu(call))
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(receive_f, cb_menu.filter(action='receive'))
    dp.register_callback_query_handler(send, cb_menu.filter(action='send'))
    dp.register_callback_query_handler(make_list_of_wallets_call, cb_menu.filter(action='wallets_call'))
    dp.register_callback_query_handler(make_wallets_menu, cb_wallet.filter())
