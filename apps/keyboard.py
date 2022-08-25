from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.common import cb_wallets, cb_menu, cb_actions
from apps.database import load_data, load_address
from localization import get_string


def menu(call: types.CallbackQuery, name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "edit"),
                             callback_data=cb_actions.new(action="edit", name=name)),
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "delete"),
                             callback_data=cb_actions.new(action="delete", name=name)),
        InlineKeyboardButton(text=get_string(call.from_user.language_code, "share"),
                             switch_inline_query=name)
    ]
    back_button = InlineKeyboardButton(text=get_string(call.from_user.language_code, "back_to_list"),
                                       callback_data=cb_menu.new(action="wallets_call"))
    keyboard.add(*buttons)
    keyboard.add(back_button)
    return keyboard


async def list_of_wallets(user_id: int):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        content = await load_data(user_id)
        for item in content:
            button = InlineKeyboardButton(text=item[0], callback_data=cb_wallets.new(name=item[0]))
            keyboard.insert(button)
        return keyboard
    except Exception as e:
        print(e)


async def clear_menu(language: str):
    try:
        keyboard = InlineKeyboardMarkup()
        back_button = InlineKeyboardButton(text=get_string(language, "clear_button"),
                                           callback_data=cb_menu.new(action="clear"))
        keyboard.add(back_button)
        return keyboard
    except Exception as e:
        print(e)


async def clear_menu_sure(language: str):
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


async def delete_menu_sure(language, name):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(text=get_string(language, "yes"),
                                 callback_data=cb_actions.new(action="yes_delete", name=name)),
            InlineKeyboardButton(text=get_string(language, "no"),
                                 callback_data=cb_menu.new(action="no_delete")),
            InlineKeyboardButton(text=get_string(language, "back"),
                                 callback_data=cb_wallets.new(name=name))
        ]
        keyboard.add(*buttons)
        return keyboard
    except Exception as e:
        print(e)


async def edit_menu(call, name):
    try:
        keyboard = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(text=get_string(call.from_user.language_code, "edit_name"),
                                 callback_data=cb_actions.new(action="edit_name", name=name)),
            InlineKeyboardButton(text=get_string(call.from_user.language_code, "edit_address"),
                                 callback_data=cb_actions.new(action="edit_address", name=name)),
            InlineKeyboardButton(text=get_string(call.from_user.language_code, "back"),
                                 callback_data=cb_wallets.new(name=name))
        ]
        keyboard.add(*buttons)
        return keyboard
    except Exception as e:
        print(e)


def cancel_button(language):
    """makes cancel button"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=get_string(language, "cancel"),
                                      callback_data=cb_menu.new(action='cancel')))
    return keyboard


def cancel_add_button(language):
    """makes cancel button while adding a wallet"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=get_string(language, "cancel"),
                                      callback_data=cb_menu.new(action='cancel_add')))
    return keyboard
