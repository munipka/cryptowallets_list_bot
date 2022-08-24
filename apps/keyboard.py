
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.common import cb_wallet, cb_menu
from apps.database import load_names
from localization import get_string


def menu(call):
    print(call.data)
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "edit"),
                             callback_data=cb_menu.new(action="edit")),
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "delete"),
                             callback_data=cb_menu.new(action="delete")),
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "share"),
                             switch_inline_query=call.data)
    ]
    back_button = InlineKeyboardButton(text=get_string(call.from_user.language_code, "back_to_list"),
                                       callback_data=cb_menu.new(action="wallets_call"))
    keyboard.add(*buttons)
    keyboard.add(back_button)
    return keyboard


async def list_of_wallets(user_id):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        content = await load_names(user_id)
        for item in content:
            button = InlineKeyboardButton(text=item[0], callback_data=cb_wallet.new(name=item[0]))
            keyboard.insert(button)
        return keyboard
    except Exception as e:
        print(e)


async def clear_menu(language):
    try:
        keyboard = InlineKeyboardMarkup()
        back_button = InlineKeyboardButton(text=get_string(language, "clear_button"),
                                           callback_data=cb_menu.new(action="clear"))
        keyboard.add(back_button)
        return keyboard
    except Exception as e:
        print(e)


async def clear_menu_sure(language):
    try:
        keyboard = InlineKeyboardMarkup()
        buttons = [
            InlineKeyboardButton(text=get_string(language, "yes"),
                                 callback_data=cb_menu.new(action="yes_clear")),
            InlineKeyboardButton(text=get_string(language, "no"),
                                 callback_data=cb_menu.new(action="no_clear")),
        ]
        keyboard.add(*buttons)
        return keyboard
    except Exception as e:
        print(e)
