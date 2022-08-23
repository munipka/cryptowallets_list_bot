import time
import telebot
from telebot import util
from telebot import types
from DBcm import UseDatabase
from itertools import chain


bot = telebot.TeleBot('5443223515:AAF9sOxM_kpS4P6-UDbROX87V4kS_1n38oQ');

adress_dict = {}
names_of_wallets=[]

dbconfig = {'host':'127.0.0.1',
             'user': 'mnep',
             'password': 'r992mma772nm',
             'database': 'telegram_bots',}

class Adress:
    def __init__(self, name):
        self.name = name
        self.adress = None


#команда /start /help
hellomsg = 'Привет, {user_name}! \n'
hellomsg += 'Команды для бота:\n'
hellomsg += "/add - добавление адреса кошелька\n"
hellomsg += '/list - список адресов\n'
hellomsg += '/wallets - редактировать кошельки\n'
hellomsg += '/clear - очистить ВСЕ данные\n'
hellomsg += 'Помимо прочего, данный бот может отправлять адреса непосредственно в чаты.'
hellomsg += ' Для этого введите @wallets_list_bot в любом чате, найдите необходимый кошелек '
hellomsg += 'и нажмите на него.'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    message = bot.send_message(message.from_user.id, hellomsg.format(
                                 user_name=message.from_user.first_name))
    
@bot.message_handler(commands=['add'])
def input_name(message):
    '''команда добавления'''
    markup = types.InlineKeyboardMarkup()
    cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
    markup.add(cancel)
    message = bot.send_message(message.chat.id,
                               '''_Постарайтесь назвать кошелек так, чтобы потом было удобно искать\. Не используйте одинаковые имена_\.
*Напишите имя кошелька:*''',
                               reply_markup=markup,
                               parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, process_name_step)
    
def process_name_step(message):
    '''добавление имени'''
    try:
        markup = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
        markup.add(cancel)
        chat_id = message.chat.id
        name = message.text
        names = list(chain.from_iterable(fetch_wallets_name(message)))
        if name in names:
            bot.send_message(message.from_user.id, 'Такое имя уже существует, введите другое!')
            input_name(message)
        else:
            wallet = Adress(name)
            adress_dict[chat_id] = wallet
            msg = bot.send_message(message.chat.id,
                                   'Напишите адрес кошелька',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, process_adress_step)  
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка, сообщите @munip')
        print(e)

def process_adress_step(message):
    '''добавление адреса'''
    try:
        chat_id = message.chat.id
        wallet = adress_dict[chat_id]
        wallet.adress = message.text
        save_adresses(wallet, chat_id)
        msg = bot.send_message(message.chat.id, '*Кошелек успешно сохранен*\!\n'
                           '/add \- добавить другой\n'
                           '/wallets \- редактировать\/удалить кошельки\n'
                           '/list \- список всех кошельков\n'
                           '/help \- показать другие команды',
                               parse_mode='MarkdownV2')
    except Exception as e:
         bot.send_message(message.chat.id, 'Произошла ошибка, сообщите @munip')
         print(e)
    
def save_adresses(wallet,chat_id):
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL ="""
                  insert into adresses (wallets_name, wallets_adress, user_id)
                  values(%s, %s, %s)
                  """
            cursor.execute(_SQL, (wallet.name,
                                  wallet.adress,
                                  chat_id, ))
    except Exception as e:
        print(e)

def fetch_wallets_name(message):
    user_id=message.chat.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_name
                      FROM adresses
                      WHERE user_id={user_id}"""
            cursor.execute(_SQL.format(user_id=user_id))
            content = cursor.fetchall()
        return content
    except Exception as e:
        print(e)

def fetch_wallets_name_call(call):
    user_id=call.message.chat.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_name
                      FROM adresses
                      WHERE user_id={user_id}"""
            cursor.execute(_SQL.format(user_id=user_id))
            content = cursor.fetchall()
        return content
    except Exception as e:
        print(e)

def fetch_wallets_adress_call(call):
    user_id=call.message.chat.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_adress
                      FROM adresses
                      WHERE user_id={user_id}
                      AND wallets_name='{wallets_name}'"""
            cursor.execute(_SQL.format(user_id=user_id, wallets_name=current_wallets_name))
            content = cursor.fetchall()
        return content
    except Exception as e:
        print(e)

@bot.message_handler(commands=['wallets'])
def wallets(message):
    try:
        content = fetch_wallets_name(message)
        buttons = list(chain.from_iterable(content))
        keyboard = types.InlineKeyboardMarkup()
        i=len(buttons)-1
        if len(buttons)==0:
            bot.send_message(message.from_user.id,'У вас еще нет сохранненых кошельков. /add - чтобы добавить"')
        else:
            if len(buttons)%2==0:
                while i>=1:
                    keyboard.add(
                        types.InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]),
                        types.InlineKeyboardButton(text=buttons[i-1], callback_data=buttons[i-1])
                        )
                    i-=2
                    if i<1:
                        break
            else:
                while i>=1:
                     keyboard.add(
                        types.InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]),
                        types.InlineKeyboardButton(text=buttons[i-1], callback_data=buttons[i-1])
                        )
                     i-=2
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(text=buttons[0], callback_data=buttons[0])
                        )
            
            bot.send_message(message.chat.id,
                            'Выберите кошелек:',
                             reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка, сообщите @munip')
        print(e)

def wallets_call(call):
    try:
        content = fetch_wallets_name_call(call)
        keyboard = telebot.types.InlineKeyboardMarkup()
        buttons = list(chain.from_iterable(content))
        keyboard = types.InlineKeyboardMarkup()
        i=len(buttons)-1
        if len(buttons)==0:
            bot.send_message(call.message.chat.id,'У вас еще нет сохранненых кошельков. /add - чтобы добавить')
        elif len(buttons)==1:
            keyboard.add(
                types.InlineKeyboardButton(text=buttons[i], callback_data=buttons[i])
                )
        else:
            if len(buttons)%2==0:
                while i>=1:
                    keyboard.add(
                        types.InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]),
                        types.InlineKeyboardButton(text=buttons[i-1], callback_data=buttons[i-1])
                        )
                    i-=2
                    if i<1:
                        break
            else:
                while i>=1:
                     keyboard.add(
                        types.InlineKeyboardButton(text=buttons[i], callback_data=buttons[i]),
                        types.InlineKeyboardButton(text=buttons[i-1], callback_data=buttons[i-1])
                        )
                     i-=2
                else:
                    keyboard.add(
                        types.InlineKeyboardButton(text=buttons[0], callback_data=buttons[0])
                        )
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Выберите кошелек:',
                              reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(call.message.chat.id, 'Произошла ошибка, сообщите @munip')
        print(e)
       
       
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        content = fetch_wallets_name_call(call)
        buttons = list(chain.from_iterable(content))
        i=len(buttons)-1
        if call.data=='cancel':
            cancel(call)
        if call.data=='wallets_list':
            wallets_call(call)
        if call.data=='delete_one_sure':
            delete_one_sure(call)
        if call.data=='delete_one':
            delete_one(call)
        if call.data=='delete_all':
            delete_all_sure(call)
        if call.data=='yes_delete_all':
            yes_delete_all(call)
        if call.data=='no_delete_all':
            no_delete_all(call)
        if call.data=='edit':
            edit_choose(call)
        if call.data=='edit_name_call':
            edit_name_call(call)
        if call.data=='edit_adress':
            edit_adress(call)
        else:
            while i >=0:
                if call.message:
                    if call.data in buttons:
                        keyboard = types.InlineKeyboardMarkup()
                        button1 = types.InlineKeyboardButton(text='Удалить', callback_data="delete_one_sure")
                        button2 = types.InlineKeyboardButton(text='Изменить', callback_data="edit")
                        button3 = types.InlineKeyboardButton(text='<-Список кошельков', callback_data='wallets_list')
                        share_button = types.InlineKeyboardButton(text='Поделиться адресом', switch_inline_query=call.data)
                        keyboard.row(button1, button2)
                        keyboard.row(share_button)
                        keyboard.row(button3)
                        global current_wallets_name, current_wallets_adress
                        current_wallets_name = call.data
                        current_wallets_adress = list(chain.from_iterable(fetch_wallets_adress_call(call)))
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                             text= 'Текущий кошелек: *{wallet}* c адресом: *{adress}* '.format(wallet=call.data,
                                                                                                           adress=current_wallets_adress[0]),
                                             reply_markup=keyboard, parse_mode="MarkdownV2")
                        bot.answer_callback_query(callback_query_id=call.id)
                        break
                    else:
                        i-=1
                        break
                break
        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print(e)
    
###команда вызова списка адресов
@bot.message_handler(commands=['list'])
def show_list(message):
    user_id = message.from_user.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_name, wallets_adress
                    FROM adresses
                    WHERE user_id={user_id}"""
            cursor.execute(_SQL.format(user_id=user_id))
            content = cursor.fetchall()
            results=''
            for item in content:
                results+='\n*Имя кошелька*: '+ item[0]
                results+= '\nАдрес кошелька:'+ '`' + item[1] + '`'
                results+= '\n'
            bot.send_message(message.from_user.id, results, parse_mode="MarkdownV2")
    except Exception as e:
        bot.send_message(message.chat.id, 'Список пуст:(')
        print(e)

def show_list_query(query):
    user_id = query.from_user.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_name, wallets_adress
                    FROM adresses
                    WHERE user_id={user_id}"""
            cursor.execute(_SQL.format(user_id=user_id))
            content = cursor.fetchall()
            results=''
            for item in content:
                results+='\n*Имя кошелька*: '+ item[0]
                results+= '\nАдрес кошелька:'+ '`' + item[1] + '`'
                results+= '\n'
            return results
    except Exception as e:
        print(e)

def delete_one_sure(call):
    try:
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Да', callback_data='delete_one')
        button2 = types.InlineKeyboardButton(text='Нет', callback_data=current_wallets_name)
        button3 = types.InlineKeyboardButton(text='<-Назад', callback_data=current_wallets_name)
        keyboard.row(button1, button2)
        keyboard.row(button3)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Текущий кошелек: {wallet}\. Удалить его?'.format(wallet=current_wallets_name),
                             reply_markup=keyboard, parse_mode="MarkdownV2")
        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print(e)

def delete_one(call):
    user_id = call.message.chat.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """DELETE FROM adresses
                      WHERE user_id={user_id}
                      AND wallets_name='{wallets_name}'"""
            cursor.execute(_SQL.format(user_id=user_id, wallets_name=current_wallets_name))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text='Кошелек удален. /wallets - изменить/удалить другие')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['clear'])
def delete_choose(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Удалить все данные', callback_data="delete_all")
        keyboard.row(button)
        bot.send_message(message.from_user.id,
                         'Нажав на кнопку, Вы удалите все данные:',
                         reply_markup=keyboard, parse_mode="MarkdownV2")
    except Exception as e:
        print(e)

def cancel(call):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Отменено')
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    except Exception as e:
        print(e)

def delete_all_sure(call):
    try:
        keyboard = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton(text='Да', callback_data="yes_delete_all")
        button2 = telebot.types.InlineKeyboardButton(text='Нет', callback_data="no_delete_all")
        keyboard.row(button1, button2)
        bot.edit_message_text(text='Вы потеряете *все данные*\. Вы уверены?',
                              chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              reply_markup=keyboard,
                              parse_mode="MarkdownV2")
        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print(e)

def yes_delete_all(call):
    delete_all(call)
    bot.answer_callback_query(callback_query_id=call.id)

def no_delete_all(call):
    send_welcome(call)
    bot.answer_callback_query(callback_query_id=call.id)
    
def delete_all(call):
    user_id = call.message.chat.id
    try:
        with UseDatabase(dbconfig) as cursor:
            _SQL = """DELETE FROM adresses
                    WHERE user_id={user_id}"""
            cursor.execute(_SQL.format(user_id=user_id))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.id,
                                  text='Данные удалены! /help')
    except Exception as e:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Произошла ошибка, либо список пуст, сообщите @munip')
        print(e)
        
def edit_choose(call):
    try:
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Изменить имя', callback_data='edit_name_call')
        button2 = types.InlineKeyboardButton(text='Изменить адрес', callback_data='edit_adress')
        button3 = types.InlineKeyboardButton(text='<-Назад', callback_data=current_wallets_name)
        keyboard.row(button1, button2)
        keyboard.row(button3)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Текущий кошелек: *{wallet}* c адресом: *{adress}* \nВыберите, что изменить:'.format(wallet=current_wallets_name,
                                                                                                           adress=current_wallets_adress[0]),
                              reply_markup=keyboard, parse_mode="MarkdownV2")
        bot.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        print(e)

def edit_name_call(call):
    try:
        markup = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
        markup.add(cancel)
        user_id = call.message.chat.id
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        message = bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.id,
                                        text='Текущее имя: *{wallet}*\nВведите новое имя кошелька'.format(wallet=current_wallets_name),
                                        reply_markup=markup,
                                        parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, process_new_name_step)
    except Exception as e:
        print(e)

def edit_name(message):
    try:
        user_id = message.chat.id
        message = bot.send_message(chat_id=message.chat.id,
                                        text='Текущее имя: *{wallet}*\nВведите новое имя кошелька'.format(wallet=current_wallets_name),
                                        parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, process_new_name_step)
    except Exception as e:
        print(e)

def process_new_name_step(message):
    try:
        user_id= message.chat.id
        new_name = message.text
        names = list(chain.from_iterable(fetch_wallets_name(message)))
        if new_name in names:
                bot.send_message(message.from_user.id, 'Такое имя уже существует, введите другое!')
                edit_name(message)
        else:
            with UseDatabase(dbconfig) as cursor:
                _SQL = """UPDATE adresses
                          SET
                          wallets_name='{new_name}'
                          WHERE
                          user_id={user_id}
                          AND
                          wallets_name='{current_wallets_name}'"""
                cursor.execute(_SQL.format(user_id=user_id,
                                           new_name=new_name,
                                           current_wallets_name=current_wallets_name))
            bot.send_message(message.chat.id, 'Имя изменено!\n /list - спикок кошельков \n /wallets-редактировать другие')
    except Exception as e:
        print(e)

def edit_adress(call):
    try:
        markup = types.InlineKeyboardMarkup()
        cancel = types.InlineKeyboardButton(text='Отмена', callback_data='cancel')
        markup.add(cancel)
        user_id = call.message.chat.id
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        message = bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.id,
                                        text='Текущий адрес: {adress}\n *Введите новый адрес кошелька:*'.format(adress=current_wallets_adress[0]),
                                        reply_markup=markup,
                                        parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, process_new_adress_step)
    except Exception as e:
        print(e)
    

def process_new_adress_step(message):
    try:
        user_id= message.chat.id
        new_adress = message.text
        with UseDatabase(dbconfig) as cursor:
            _SQL = """UPDATE adresses
                      SET
                      wallets_adress='{new_adress}'
                      WHERE
                      user_id={user_id}
                      AND
                      wallets_name='{current_wallets_name}'"""
            cursor.execute(_SQL.format(user_id=user_id,
                                       new_adress=new_adress,
                                       current_wallets_name=current_wallets_name))
        bot.send_message(message.chat.id, 'Адрес кошелька изменен!')
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text:
        send_welcome(message)

@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    try:
        msg=show_list_query(query)
        r = types.InlineQueryResultArticle(
                id='1',
                title="Список кошельков",
                description='Отправить список ВСЕХ моих кошельков',
                input_message_content=types.InputTextMessageContent(
                                                                    message_text=show_list_query(query),
                                                                    parse_mode="MarkdownV2"
                                                                    )
                
                )
        r2 = types.InlineQueryResultArticle(
                id='2',
                title='Помощь',
                input_message_content=types.InputTextMessageContent(
                    message_text=
                    'В любом чате напишите @wallets_list_bot, введите имя кошелька и нажмите, чтобы отправить его'),
        )
        bot.answer_inline_query(query.id, [r,r2], cache_time=0, is_personal=True,
                                switch_pm_text='Добавить новый',
                                switch_pm_parameter='add')
    except Exception as e:
        print(e)
        
def get_wallet(query):
    try:
        user_id = query.from_user.id
        search_query = query.query
        with UseDatabase(dbconfig) as cursor:
            _SQL = """SELECT wallets_name, wallets_adress
                    FROM adresses
                    WHERE user_id={user_id}
                    AND wallets_name LIKE '%{search_query}%'"""
            cursor.execute(_SQL.format(user_id=user_id, search_query=search_query))
            content = cursor.fetchall()
            results=''
            for item in content:
                results+='\n*Имя кошелька*: '+ item[0]
                results+= '\nАдрес кошелька:'+ '`' + item[1] + '`'
            return content
    except Exception as e:
        print(e)

@bot.inline_handler(func=lambda query: len(query.query) > 0)
def not_empty_query(query):
    try:
        wallets= get_wallet(query)
        wallets = list(chain.from_iterable(wallets))
        if len(wallets)==0:
            switch_text='Не найдено, нажмите, чтобы добавить'
            bot.answer_inline_query(query.id, results=[], cache_time=0,
                                           switch_pm_text=switch_text,
                                           switch_pm_parameter='add')
        if len(wallets)>0:
            i = len(wallets)-1
            articles=[]
            while i>=0:
                articles.append(types.InlineQueryResultArticle(
                        id=len(wallets)-i,
                        title=str('Имя: '+ wallets[i-1]),
                        description=str('Адрес: '+ wallets[i]),
                        input_message_content=types.InputTextMessageContent(
                                                                            message_text='\n*Имя кошелька*: '+ wallets[i-1]+
                                                                            '\nАдрес кошелька:'+'`'+wallets[i]+'`',
                                                                            parse_mode="MarkdownV2",
                                                                            ),
                    
                    ) )
                i-=2
            
            help_article = types.InlineQueryResultArticle(
                    id =len(wallets),
                    title='Помощь',
                    input_message_content=types.InputTextMessageContent(
                        message_text=
                        'В любом чате напишите @wallets_list_bot, введите имя кошелька и нажмите на него, чтобы отправить его'),
            )
            articles.append(help_article)
            bot.answer_inline_query(query.id, articles, cache_time=0,
                                           switch_pm_text='Добавать новый',
                                           switch_pm_parameter='add')
        
    except Exception as e:
        print(e)
            
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

