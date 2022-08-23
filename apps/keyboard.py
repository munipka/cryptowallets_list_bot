from itertools import chain

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.common import cb_wallet, cb_menu
from apps.database import load_names
from localization import get_string


def menu(language):
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text=get_string(language, "edit"),
                             callback_data=cb_menu.new(action="edit")),
        InlineKeyboardButton(text=get_string(language, "delete"),
                             callback_data=cb_menu.new(action="delete"))
    ]
    keyboard.add(*buttons)
    return keyboard


async def list_of_wallets(message):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        content = await load_names(message.from_user.id)
        for item in content:
            button = InlineKeyboardButton(text=item[0], callback_data=cb_wallet.new(name=item[0]))
            keyboard.insert(button)
        return keyboard
    except Exception as e:
        print(e)
