from collections import defaultdict


def get_language(lang_code) -> str:
    """returns language code"""
    langs = defaultdict(lambda: "en", {"ru": "ru"})
    return langs[lang_code.split("-")[0]] if lang_code else "en"


def get_string(lang_code: str, string_id: str) -> str:
    """returns a string according to string_id"""
    lang = get_language(lang_code)
    try:
        return all_strings[lang][string_id]
    except KeyError:
        return "ERR_NO_STRING"


en_text_start = """Hi!\nCommands for the bot:\n/add - add wallet
/list - address list\n/wallets - edit wallets\n/clear - clear ALL data\n\n
Among other things, this bot can send addresses directly to chats.
To do this, enter @wallets_list_bot in any chat, find the necessary wallet and click on it."""

en_add_name = """_Try to name the wallet so that it is convenient to search for it later\.
⚠Do not use the names already used\._
*Write the name of the wallet:*"""

en_added = """✅The wallet has been successfully added!\n/add - add another one
/list - list of all wallets
/wallets - edit data\n/help - bot commands"""

ru_text_start = """Привет!\nКоманды для бота:\n/add - добавить кошелёк
/list - список кошельков\n/wallets - редактировать кошельки\n/clear - очистить ВСЕ данные\n\n
Помимо прочего, данный бот может отправлять адреса непосредственно в чаты.
Для этого введите @wallets_list_bot в любом чате, найдите необходимый кошелек и нажмите на него."""

ru_add_name = """_Постарайтесь назвать кошелек так, чтобы потом было удобно его искать\.
⚠Не используйте уже использованные имена\._
*Напишите имя кошелька:*"""

ru_added = """✅Кошелек успешно добавлен!\n/add - добавить еще один
/list - список всех кошельков
/wallets - редактировать данные\n/help - команды бота"""

all_strings = {
    "en": {
        "start": en_text_start,
        "help": en_text_start,
        "add_wallet_name": en_add_name,
        "add_wallet_address": "Name entered!\n\nNow enter the address:",
        "added": en_added,
        "wal_name": "Wallet name: ",
        "wal_address": "Wallet address: ",
        "list": "List of all wallets",
        "help_query": "Help",
        "help_query_text": "In any chat, write @wallets_list_bot, enter the wallet name and click to send it",
        "empty_list": "⚠You don't have any saved wallets yet.\n/add - to add a wallet",
        "empty_list_query": "The list is empty, click here➕",
        "found_nothing": "Not found with this name",
        "add_new": "➕Add new",
        "clear": "By clicking on the button, you will delete *all* data:",
        "clear_button": "❌Delete all data!",
        "clear_sure": "⚠You will lose all data! Are you sure?",
        "cleared": "All data has been deleted!\n/help - view commands",
        "wallets": "Choose one of your saved wallets:",
        "edit": "✏Edit",
        "edit_choice": "Current name: *{}*\nCurrent address: {}",
        "edit_name": "✏Edit name",
        "edit_name_process": "Current wallet name: {}\n_Enter a new name:_",
        "edit_name_set": "✅The name has been changed!\n\n/help - view commands\n/wallets - edit wallets",
        "name_exists": "⚠A wallet with that name already exists!\nEnter another name:",
        "edit_address": "✏Edit address",
        "edit_address_process": "_Enter a new address:_",
        "edit_address_set": "✅The address has been changed!\n\n/help - view commands\n/wallets - edit wallets",
        "delete": "❌Delete",
        "delete_sure": "⚠Do you really want to delete the wallet *{}*?",
        "deleted": "You deleted the wallet *{}*\!\n\n/help \- bot commands",
        "share": "Share wallet",
        "back_to_list": "<- Back to the list",
        "back": "<- Back",
        "no": "No",
        "yes": "Yes",
        "cancel": "Cancel",
        "canceled": "The operation was canceled!\n/help - view commands"
    },
    "ru": {
        "start": ru_text_start,
        "help": ru_text_start,
        "add_wallet_name": ru_add_name,
        "add_wallet_address": "Имя введено!\n\nТеперь введите адрес:",
        "added": ru_added,
        "wal_name": "Имя кошелька: ",
        "wal_address": "Адрес кошелька: ",
        "list": "Список всех кошельков",
        "help_query": "Помощь",
        "help_query_text": "В любом чате напишите @wallets_list_bot, введите имя кошелька и нажмите, чтобы отправить его",
        "empty_list": "⚠У вас еще нет сохранненых кошельков.\n/add - чтобы добавить",
        "empty_list_query": "Список пуст, нажмите➕",
        "found_nothing": "Не найдено с таким именем",
        "add_new": "➕Добавить новый",
        "clear": "Нажав на кнопку, Вы удалите *все* данные:",
        "clear_button": "❌Удалить все данные!",
        "clear_sure": "⚠Вы потеряете все данные! Вы уверены?",
        "cleared": "Все данные были удалены!\n/help - посмотреть команды",
        "wallets": "Выберите один из своих сохраненных кошельков:",
        "edit": "✏Изменить",
        "edit_choice": "Текущее имя: *{}*\nТекущий адрес: {}",
        "edit_name": "✏Изменить имя",
        "edit_name_process": "Текущее имя кошелька: {}\n_Введи новое имя:_",
        "edit_name_set": "✅Имя было изменено!\n\n/help - посмотреть команды\n/wallets - редактировать кошельки",
        "name_exists": "⚠Кошелек с таким именем уже существует!\nВведите другое имя:",
        "edit_address": "✏Изменить адрес",
        "edit_address_process": "_Введите новый адрес:_",
        "edit_address_set": "✅Адрес был изменен!\n\n/help - посмотреть команды\n/wallets - редактировать кошельки",
        "delete": "❌Удалить",
        "delete_sure": "⚠Вы действительно хотите удалить кошелек *{}*?",
        "deleted": "Вы удалили кошелек *{}*\!\n\n/help \- команды бота",
        "share": "Поделиться адресом",
        "back_to_list": "<- Назад к списку",
        "back": "<- Назад",
        "no": "Нет",
        "yes": "Да",
        "cancel": "Отмена",
        "canceled": "Операция была отменена!\n/help - посмотреть команды"
    }
}
