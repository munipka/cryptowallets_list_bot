from aiogram import Dispatcher, types
from apps.keyboard import menu
from localization import get_string
from apps.database import load_data, load_names

from apps.keyboard import list_of_wallets, clear_menu


async def cmd_start(message: types.Message):
    await message.answer(get_string(message.from_user.language_code, "start"))


async def add(message: types.Message):
    await message.answer(get_string(message.from_user.language_code, "add"))


async def show_list(message: types.Message):
    try:
        content = await load_data(message.from_user.id)
        results = ''
        for item in content:
            results += '\n*' + get_string(message.from_user.language_code, 'wal_name') + '* ' + item[0]
            results += '\n' + get_string(message.from_user.language_code, 'wal_address') + ' ' + '`' + item[1] + '`'
            results += '\n'
        await message.answer(results, parse_mode="MarkdownV2")
    except Exception as e:
        await message.answer(get_string(message.from_user.language_code, 'empty_list'))
        print(e)


async def clear(message: types.Message):
    try:
        await message.answer(get_string(message.from_user.language_code, "clear"),
                             parse_mode="MarkdownV2",
                             reply_markup=await clear_menu(message.from_user.language_code))
    except Exception as e:
        print(e)


async def wallets(message: types.Message):
    try:
        if len(await load_names(message.from_user.id)) == 0:
            await message.answer(get_string(message.from_user.language_code, 'empty_list'))
        else:
            await message.answer(get_string(message.from_user.language_code, "wallets"),
                                 reply_markup=await list_of_wallets(message.from_user.id))
    except Exception as e:
        print(e)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start", "help"])
    dp.register_message_handler(add, commands='add')
    dp.register_message_handler(show_list, commands='list')
    dp.register_message_handler(clear, commands='clear')
    dp.register_message_handler(wallets, commands='wallets')
