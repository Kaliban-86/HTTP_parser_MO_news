import telebot
from HTTP_parser import take_news_to_list
from telebot import types
from main import all_lessons
import datetime

with open('token.txt', 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)
id_list = [1201776385, 0, 0]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id in id_list:
        bot.reply_to(message,
                     f'Добро пожаловать, я телебот MO_RF, могу рассказать тебе последние новости МО РФ!')
    else:
        bot.reply_to(message, 'Вам отказано в доступе!!! Свяжитесь с администратором бота!!!')


@bot.message_handler(commands=['info'])
def show_info(message):
    if message.chat.id in id_list:
        bot.reply_to(message,
                     f'Бот предназначен для публикации новостей по теме "МО РФ" с новостоного портала РБК')
    else:
        bot.reply_to(message, 'Вам отказано в доступе!!! Свяжитесь с администратором бота!!!')


@bot.message_handler(commands=['learning'])
def take_timetable(message):
    if message.chat.id in id_list:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='today')
        item2 = types.InlineKeyboardButton(text='Расписание на завтра', callback_data='tomorrow')
        item3 = types.InlineKeyboardButton(text='Расписание сессии', callback_data='session')

        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, 'Что вы хотите посмотреть?', reply_markup=markup)
    else:
        bot.reply_to(message, 'Вам отказано в доступе!!! Свяжитесь с администратором бота!!!')


@bot.message_handler(commands=['news'])
def send_welcome(message):
    if message.chat.id in id_list:
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Все новости", callback_data='all')
        item2 = types.InlineKeyboardButton(text="10 последних новостей", callback_data='ten')
        item3 = types.InlineKeyboardButton(text="5 последних новостей", callback_data='five')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, 'Сколько показать новостей?', reply_markup=markup)
    else:
        bot.reply_to(message, 'Вам отказано в доступе!!! Свяжитесь с администратором бота!!!')


def show_lesson_to_bot(lesson_list, call):
    date = str(lesson_list[0])
    first_lesson = 'первая пара - ' + str(lesson_list[1])
    second_lesson = 'вторая пара - ' + str(lesson_list[2])
    third_lesson = 'третья пара - ' + str(lesson_list[3])
    bot.send_message(call.message.chat.id, f'{date}\n{first_lesson}\n{second_lesson}\n{third_lesson}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    new_list = take_news_to_list()
    lessons = all_lessons
    curr_date = datetime.date.today()
    tomorrow_date = datetime.datetime(curr_date.year, curr_date.month, curr_date.day + 1)
    if call.message:
        if call.data == 'all':
            for one_news in reversed(new_list):
                bot.send_message(call.message.chat.id, f'{one_news.news_url}')

        elif call.data == 'ten':
            for one_news in reversed(new_list[:10]):
                bot.send_message(call.message.chat.id, f'{one_news.news_title} {one_news.news_url}')

        elif call.data == 'five':
            for one_news in reversed(new_list[:5]):
                bot.send_message(call.message.chat.id, f'{one_news.news_title} {one_news.news_url}')

        elif call.data == 'today':
            for i in lessons:
                if curr_date == i[0]:
                    show_lesson_to_bot(i, call)

        elif call.data == 'tomorrow':
            for i in lessons:
                if str(tomorrow_date.date()) == i[0]:
                    show_lesson_to_bot(i, call)


@bot.message_handler(content_types=['text'])
def about_tex(message):
    bot.reply_to(message, f'Команда - "{message.text}" не предусмотрена программой данного бота')


bot.polling(none_stop=True)
