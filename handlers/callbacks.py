from aiogram import types, Dispatcher
from aiogram.utils import callback_data

from apps.common import cb_menu, cb_wallets, cb_actions
from apps.database import load_address, delete_all, delete_one
from localization import get_string

from apps.keyboard import menu, list_of_wallets, clear_menu_sure, delete_menu_sure, edit_menu


async def launch_list_of_wallets_call(call: types.CallbackQuery):
    try:
        await call.message.edit_text(text=get_string(call.from_user.language_code, "wallets"),
                                     reply_markup=await list_of_wallets(call.from_user.id))
        await call.answer()
    except Exception as e:
        print(e)


async def launch_wallet_menu_call(call: types.CallbackQuery, callback_data: dict):
    name = callback_data["name"]
    address = await load_address(call.from_user.id, name)
    text = get_string(call.from_user.language_code, 'wal_name') + f' *{name}*\n'
    text += get_string(call.from_user.language_code, 'wal_address') + f'*{address[0][0]}*'
    await call.message.edit_text(text, parse_mode="MarkdownV2", reply_markup=menu(call, name))
    await call.answer()


async def launch_edit_menu_call(call: types.CallbackQuery, callback_data: dict):
    try:
        name = callback_data["name"]
        address = await load_address(call.from_user.id, name)
        text = get_string(call.from_user.language_code, 'edit_choice')
        await call.message.edit_text(text.format(name, address[0][0]), parse_mode="MarkdownV2",
                                     reply_markup=await edit_menu(call, name))
    except Exception as e:
        print(e)


async def launch_delete_menu_call(call: types.CallbackQuery, callback_data: dict):
    try:
        name = callback_data["name"]
        text = get_string(call.from_user.language_code, 'delete_sure')
        await call.message.edit_text(text=text.format(name),
                                     parse_mode="MarkdownV2",
                                     reply_markup=await delete_menu_sure(call.from_user.language_code, name))
        await call.answer()
    except Exception as e:
        print(e)


async def yes_delete(call: types.CallbackQuery, callback_data: dict):
    try:
        name = callback_data["name"]
        await delete_one(call.from_user.id, name)
        text = get_string(call.from_user.language_code, 'deleted')
        await call.message.edit_text(text=text.format(name), parse_mode="MarkdownV2")
        await call.answer()
    except Exception as e:
        print(e)


async def cancel(call: types.CallbackQuery):
    await call.message.edit_text(get_string(call.from_user.language_code, "canceled"))
    await call.answer()


async def launch_clear_menu_call(call: types.CallbackQuery):
    await call.message.edit_text(get_string(call.from_user.language_code, 'clear_sure'),
                                 reply_markup=await clear_menu_sure(call.from_user.language_code))
    await call.answer()


async def yes_clear(call: types.CallbackQuery):
    await delete_all(call.from_user.id)
    await call.message.edit_text(get_string(call.from_user.language_code, "cleared"))
    await call.answer()


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(launch_list_of_wallets_call, cb_menu.filter(action='wallets_call'))
    dp.register_callback_query_handler(launch_clear_menu_call, cb_menu.filter(action='clear'))
    dp.register_callback_query_handler(yes_clear, cb_menu.filter(action='yes_clear'))
    dp.register_callback_query_handler(cancel, cb_menu.filter(action='no_clear'))
    dp.register_callback_query_handler(launch_delete_menu_call, cb_actions.filter(action='delete'))
    dp.register_callback_query_handler(yes_delete, cb_actions.filter(action='yes_delete'))
    dp.register_callback_query_handler(cancel, cb_menu.filter(action='no_delete'))
    dp.register_callback_query_handler(launch_edit_menu_call, cb_actions.filter(action='edit'))
    dp.register_callback_query_handler(launch_wallet_menu_call, cb_wallets.filter())
