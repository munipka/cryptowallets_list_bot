from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from apps.common import cb_menu, cb_actions
from apps.keyboard import cancel_button
from apps.database import update_name, load_names, update_address

from localization import get_string

from itertools import chain


class EditName(StatesGroup):
    old_name = State()
    new_name = State()


class EditAddress(StatesGroup):
    old_name = State()
    new_address = State()


async def edit_name_start(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        old_name = callback_data["name"]
        text = get_string(call.from_user.language_code, "edit_name_process")
        await EditName.new_name.set()
        await state.update_data(old_name=old_name)
        await call.message.edit_text(text.format(old_name), reply_markup=cancel_button(), parse_mode="MarkdownV2")
        await call.answer()
    except Exception as e:
        print(e)


async def new_name_set(message, state: FSMContext):
    try:
        names_already_exist = list(chain.from_iterable(await load_names(message.from_user.id)))
        if message.text in names_already_exist:
            await message.answer(get_string(message.from_user.language_code, "name_exists"),
                                 reply_markup=cancel_button())
            return
        else:
            await state.update_data(new_name_set=message.text)
            data = await state.get_data()
            old_name = data['old_name']
            new_name = message.text
            await update_name(message.from_user.id, old_name, new_name)
            text = get_string(message.from_user.language_code, "edit_name_set")
            await message.answer(text)
            await state.finish()
    except Exception as e:
        print(e)


async def edit_address_start(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        old_name = callback_data["name"]
        text = get_string(call.from_user.language_code, "edit_address_process")
        await EditAddress.new_address.set()
        await state.update_data(old_name=old_name)
        await call.message.edit_text(text.format(old_name), reply_markup=cancel_button(), parse_mode="MarkdownV2")
        await call.answer()
    except Exception as e:
        print(e)


async def new_address_set(message, state: FSMContext):
    try:
        await state.update_data(new_address_set=message.text)
        data = await state.get_data()
        old_name = data['old_name']
        new_address = message.text
        await update_address(message.from_user.id, old_name, new_address)
        text = get_string(message.from_user.language_code, "edit_address_set")
        await message.answer(text)
        await state.finish()
    except Exception as e:
        print(e)


async def cancel(call, state):
    try:
        keyboard = types.InlineKeyboardMarkup()
        text = get_string(call.from_user.language_code, "back_to_list")
        keyboard.add(types.InlineKeyboardButton(text=text,
                                                callback_data=cb_menu.new(action='wallets_call')))
        await call.message.edit_text(text=get_string(call.from_user.language_code, "canceled"),
                                     reply_markup=keyboard)
        await state.finish()
        await call.answer()
    except Exception as e:
        print(e)


def register_state_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(edit_name_start, cb_actions.filter(action="edit_name"))
    dp.register_message_handler(new_name_set, state=EditName.new_name)
    dp.register_callback_query_handler(edit_address_start, cb_actions.filter(action="edit_address"))
    dp.register_message_handler(new_address_set, state=EditAddress.new_address)
    dp.register_callback_query_handler(cancel, cb_menu.filter(action='cancel'), state='*')
