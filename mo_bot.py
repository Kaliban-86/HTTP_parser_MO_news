import telebot
from HTTP_parser import take_news_to_list
from telebot import types
from main import all_lessons
import sqlite3

with open('token.txt', 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Добро пожаловать, я телебот MO_RF, могу рассказать тебе последние новости МО РФ!')


@bot.message_handler(commands=['info'])
def show_info(message):
    bot.reply_to(message,
                 f'Бот предназначен для побликации подборки новостей по теме "МО РФ" с новостоного портала РБК')


@bot.message_handler(commands=['learning'])
def take_timetable(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='today')
    item2 = types.InlineKeyboardButton(text='Расписание на завтра', callback_data='tomorrow')
    item3 = types.InlineKeyboardButton(text='Расписание сессии', callback_data='session')

    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(message.chat.id, 'Что вы хотите посмотреть?', reply_markup=markup)


@bot.message_handler(commands=['news'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Все новости", callback_data='all')
    item2 = types.InlineKeyboardButton(text="10 последних новостей", callback_data='ten')
    item3 = types.InlineKeyboardButton(text="5 последних новостей", callback_data='five')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(message.chat.id, 'Сколько показать новостей?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    new_list = take_news_to_list()
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
        elif call.data == 'session':
            lessons = all_lessons
            date = str(lessons[0][0])
            first_lesson = 'первая пара - ' + str(lessons[0][1])
            second_lesson = 'вторая пара - ' + str(lessons[0][2])
            third_lesson = 'третья пара - ' + str(lessons[0][3])
            bot.send_message(call.message.chat.id, f'{date}\n{first_lesson}\n{second_lesson}\n{third_lesson}')


@bot.message_handler(content_types=['text'])
def about_tex(message):
    bot.reply_to(message, f'Команда - "{message.text}" не предусмотрена программой данного бота')


bot.polling(none_stop=True)
