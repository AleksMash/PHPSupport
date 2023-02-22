import telebot
import time

from telebot import types
from telebot.util import quick_markup
from environs import Env

import db

CLIENT_GREET = "Привет тебе, дорогой клиент!"
EXEC_GREET = "Привет тебе, дорогой исполнитель!"
ADMIN_GREET = "Привет тебе, о великий Админ!"

env = Env()
env.read_env()

tg_clients_token = env('TG_BOT_TOKEN')
client_bot = telebot.TeleBot(token=tg_clients_token)

markup_client = quick_markup({
    'Мои заявки': {'callback_data': 'apps_to_client'},
    'Подать заявку':{'callback_data': 'apply'}
})
markup_executor = quick_markup({
    'Список заказов': {'callback_data': 'apps_to_exec'},
    'Условия оплаты': {'callback_data': 'salary'},
    'Что я делаю': {'callback_data': 'active_task'},
    'Задать вопрос':{'callback_data': 'ask_question'},
    'Сдать работу': {'callback_data': 'work_done'}
})


def get_time_conv():
    return lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


@client_bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    print(message.text)
    access, type = db.check_access_by_tgname(message.from_user.username)
    if access==-1:
        client_bot.send_message(message.chat.id, 'Вы не зарегистрированы в системе.')
    elif access==0 and type == db.UT_CLIENT:
        client_bot.send_message(message.chat.id, 'Ваша подписка окончилась, новые заявки создать нельзя.'
                                                 'Однако можно отслеживать ранее поданные заявки')
    elif access==1:
        if type==0:
            client_bot.send_message(message.chat.id, ADMIN_GREET)
            client_bot.send_message(message.chat.id, "Меню админа в разработке")
        elif type==1:
            client_bot.send_message(message.chat.id, CLIENT_GREET)
            client_bot.send_message(message.chat.id, "Основное меню:", reply_markup=markup_client)
        elif type==2:
            client_bot.send_message(message.chat.id, EXEC_GREET)
            client_bot.send_message(message.chat.id, "Основное меню", reply_markup=markup_executor)


#сделать обработчики других команд, описанных в инфо

#сделать обработчик текстовый сообщений (ввод инфы от пользователя) c ветвлением на основании алгоритма,
#либо сделать как показано здесь: https://habr.com/ru/post/442800/ - см. раздел ветки сообщений.


@client_bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)
    #здесь ведем обработку нажатий кнопок.
    #имеем ввиду что при ответе на кнопки некоторые сообщения
    #оснащаются другими кнопками которые также обрабатываются здесь,
    #либо для них надо сделать индивидуальные обработчики .... решить.





client_bot.polling(none_stop=True, interval=0)
