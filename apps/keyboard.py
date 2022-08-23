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
        keyboard = InlineKeyboardMarkup()
        content = await load_names(message.from_user.id)
        buttons = list(chain.from_iterable(content))

        i = len(buttons) - 1

        if len(content) == 0:
            await message.answer(get_string(message.from_user.language_code, "empty_list"))

        elif len(content) == 1:
            keyboard.add(
                InlineKeyboardButton(text=buttons[i], callback_data=cb_wallet.new(name=buttons[i]))
            )
        if len(content) % 2 == 0:
            while i >= 1:
                keyboard.add(
                    InlineKeyboardButton(text=buttons[i], callback_data=cb_wallet.new(name=buttons[i])),
                    InlineKeyboardButton(text=buttons[i - 1], callback_data=cb_wallet.new(name=buttons[i - 1]))
                )
                i -= 2
                if i < 1:
                    break
        else:
            while i >= 1:
                keyboard.add(
                    InlineKeyboardButton(text=buttons[i], callback_data=cb_wallet.new(name=buttons[i])),
                    InlineKeyboardButton(text=buttons[i - 1], callback_data=cb_wallet.new(name=buttons[i - 1]))
                )
                i -= 2
            else:
                keyboard.add(
                    InlineKeyboardButton(text=buttons[0], callback_data=cb_wallet.new(name=buttons[0]))
                )
        return keyboard
    except Exception as e:
        print(e)
