from itertools import chain

from aiogram import types, Dispatcher
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from apps.database import load_data, search_wallet
from localization import get_string

list_icon = 'https://i.ibb.co/fXDV3XX/list.png'
help_icon = 'https://i.ibb.co/sWQQKbb/help.png'


async def show_list_query(query: types.InlineQuery):
    """Inline query handler of an empty query"""
    try:
        content = await load_data(query.from_user.id)
        if len(content) == 0:
            text = get_string(query.from_user.language_code, 'empty_list_query')
            return await query.answer(results=[], cache_time=0,
                                      switch_pm_text=text,
                                      switch_pm_parameter='add')
        else:
            results = ''
            for item in content:
                results += '\n*' + get_string(query.from_user.language_code, 'wal_name') + '* ' + item[0]
                results += '\n' + get_string(query.from_user.language_code, 'wal_address') + ' ' + '`' + item[1] + '`'
                results += '\n'
            return results
    except Exception as e:
        print(e)


async def inline_send_wallet(query: types.InlineQuery):
    """Inline query handler of not empty query. Handles searching query in a database and returns results"""
    try:
        if len(query.query) == 0:
            text = await show_list_query(query)
            input_content = InputTextMessageContent(text, parse_mode="MarkdownV2")
            item = InlineQueryResultArticle(
                id='1',
                title=get_string(query.from_user.language_code, 'list'),
                input_message_content=input_content,
                thumb_url=list_icon,
                thumb_width=48, thumb_height=48
            )
            help_item = types.InlineQueryResultArticle(
                id='2',
                title=get_string(query.from_user.language_code, 'help_query'),
                input_message_content=types.InputTextMessageContent(
                    message_text=get_string(query.from_user.language_code, 'help_query_text')),
                thumb_url=help_icon,
                thumb_width=48, thumb_height=48
            )
            await query.answer(results=[item, help_item], cache_time=1)
        if len(query.query) > 0:
            search_query = query.query
            results = await search_wallet(query.from_user.id, search_query)
            results = list(chain.from_iterable(results))
            if len(results) == 0:
                switch_text = get_string(query.from_user.language_code, 'found_nothing')
                await query.answer(results=[], cache_time=0,
                                   switch_pm_text=switch_text,
                                   switch_pm_parameter='add')
            elif len(results) > 0:
                i = len(results) - 1
                articles = []
                while i >= 0:
                    articles.append(types.InlineQueryResultArticle(
                        id=str(len(results) - i),
                        title=str(get_string(query.from_user.language_code, 'wal_name') + results[i - 1]),
                        description=str(get_string(query.from_user.language_code, 'wal_address') + results[i]),
                        input_message_content=types.InputTextMessageContent(
                            message_text=get_string(query.from_user.language_code, 'wal_name') + results[i - 1] + '\n' +
                                         get_string(query.from_user.language_code, 'wal_address') + '`' + results[i] + '`',
                            parse_mode="MarkdownV2",
                        ),

                    ))
                    i -= 2

                help_article = types.InlineQueryResultArticle(
                    id=str(len(results)),
                    title=get_string(query.from_user.language_code, 'help_query'),
                    input_message_content=types.InputTextMessageContent(
                        message_text=get_string(query.from_user.language_code, 'help_query_text')),
                    thumb_url=help_icon,
                    thumb_width=48, thumb_height=48
                )
                articles.append(help_article)
                await query.answer(articles, cache_time=0,
                                   switch_pm_text=get_string(query.from_user.language_code, 'add_new'),
                                   switch_pm_parameter='add')
    except Exception as e:
        print(e)


def register_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_send_wallet)
    dp.register_inline_handler(show_list_query)
