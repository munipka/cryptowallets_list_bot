from collections import defaultdict


def get_language(lang_code) -> str:
    """returns language code"""
    langs = defaultdict(lambda: "en", {"ru": "ru"})
    return langs[lang_code.split("-")[0]] if lang_code else "en"


def get_string(lang_code: str, string_id: str) -> str:
    lang = get_language(lang_code)
    try:
        return all_strings[lang][string_id]
    except KeyError:
        # TODO: log this error
        return "ERR_NO_STRING"


en_text_start = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
You can use this bot to generate <a href="http://xkcd.com/936/">readable passwords</a>.
Press "[ / ]" to choose from presets of different strength or use /generate command to send " \
custom password (configurable in /settings)
If you would like to see the source code or get help, simply press /help."""

en_text_settings_choose = """Here are your current settings:
<b>Number of words</b>: {num_of_words!s}
<b>Extra prefixes/suffixes</b>: {prefixes}
<b>Separators between words</b>: {separators}
You can edit these settings using buttons below.
After you're satisfied with results, use /generate command"""

en_text_help = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
The idea of this bot came from <a href="http://xkcd.com/936/">XKCD 936</a> strip. So I decided to make \
a bot which will help me quickly generate strong and readable passwords without having me open " \
KeePass or any other app."""

ru_text_help = """<a href="http://imgs.xkcd.com/comics/password_strength.png">&#8203;</a>\
Идея по созданию этого бота пришла ко мне после прочтения комикса <a href="http://xkcd.com/936/">XKCD 936</a>. \
После чего я решил создать инструмент для удобной генерации сложных, но читабельных паролей без необходимости \
открывать KeePass или что-либо ещё."""

ru_text_start = """Привет!\nКоманды для бота:\n/add - добавление адреса кошелька
/list - список адресов\n/wallets - редактировать кошельки\n/clear - очистить ВСЕ данные\n
Помимо прочего, данный бот может отправлять адреса непосредственно в чаты.
Для этого введите @wallets_list_bot в любом чате, найдите необходимый кошелек и нажмите на него."""

ru_add = """Постарайтесь назвать кошелек так, чтобы потом было удобно искать. Не используйте одинаковые имена.
Напишите имя кошелька:"""

ru_text_settings_choose = """Ваши настройки:
<b>Количество слов</b>: {num_of_words!s}
<b>Префиксы/суффиксы</b>: {prefixes}
<b>Разделители между словами</b>: {separators}
Используйте кнопки ниже для изменения настроек.
Затем вызовите команду /generate для генерации пароля с этими настройками."""

all_strings = {
    "en": {
        "start": en_text_start,
        "help": en_text_help,
        "settings": en_text_settings_choose,
        "plusword": "+ word",
        "minusword": "- word",
        "pluspref": "Add prefix & suffix",
        "minuspref": "Remove prefix & suffix",
        "plussep": "Add separators",
        "minussep": "Remove separators",
        "regenerate": "🔄 Regenerate",
        "no": "No",
        "yes": "Yes",
        "inline_weak_title": "Weak password",
        "inline_weak_description": "2 words, no digits or separators",
        "inline_normal_title": "Normal password",
        "inline_normal_description": "3 words, random UPPERCASE, separated by numbers",
        "inline_strong_title": "Strong password",
        "inline_strong_description": "4 words, random UPPERCASE, separated by numbers or special characters"
    },
    "ru": {
        "start": ru_text_start,
        "help": ru_text_help,
        "settings": ru_text_settings_choose,
        "add": ru_add,
        "wal_name": "Имя кошелька:",
        "wal_address": "Адрес кошелька:",
        "empty_list": "У вас еще нет сохранненых кошельков.\n/add - чтобы добавить",
        "clear": "Нажав на кнопку, Вы удалите *все* данные:",
        "clear_button": "Удалить все данные!",
        "clear_sure": "Вы потеряете все данные! Вы уверены?",
        "cleared": "Все данные были удалены!\n/help - посмотреть команды",
        "wallets": "Выберите один из своих сохраненных кошельков:",
        "edit": "Изменить",
        "delete": "Удалить",
        "delete_sure": "Вы действительно хотите удалить кошелек *{}*?",
        "deleted": "Вы удалили кошелек *{}*\!\n/help \- команды бота",
        "share": "Поделиться",
        "back_to_list": "<- Назад к списку",
        "back": "<- Назад",
        "regenerate": "🔄 Новый пароль",
        "no": "Нет",
        "yes": "Да",
        "canceled": "Операция была отменена!\n/help - посмотреть команды",
        "": "Слабый пароль",
        "inline_weak_description": "2 слова строчными буквами, без разделителей",
        "inline_normal_title": "Средний пароль",
        "inline_normal_description": "3 слова, случайных выбор ПРОПИСНЫХ слов, случайные цифры в качестве разделителей",
        "inline_strong_title": "Надёжный пароль",
        "inline_strong_description": "4 слова, случайных выбор ПРОПИСНЫХ слов, цифры и спецсимволы в качестве разделителей"
    }
}
