import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
import sqlite3
import datetime
import os

# from config import TOKEN

conn = sqlite3.connect('studies.db')

cursor = conn.cursor()

cursor.execute('SELECT * from lessons')

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.first_lesson = d.id and l.first_lesson_type = ct.id ')

first_lesson_res = cursor.fetchall()

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.second_lesson = d.id and l.second_lesson_type = ct.id')

second_lesson_res = cursor.fetchall()

cursor.execute(
    'select l.date, d.name, ct.class from lessons l, disciplines d, class_type ct where l.third_lesson = d.id and l.third_lesson_type = ct.id')

third_lesson_res = cursor.fetchall()

sum_lessons_res = []


def concat_lesson(first_lessons, second_lessons, third_lesson):
    res_lessons = []

    for k in range(len(first_lessons)):
        if first_lessons[k][0] == second_lessons[k][0] == third_lesson[k][0]:
            day_lessons = [first_lessons[k][0], str(first_lessons[k][1]) + ' (' + str(first_lessons[k][2]) + ')',
                           str(second_lessons[k][1]) + ' (' + str(second_lessons[k][2]) + ')',
                           str(third_lesson[k][1]) + ' (' + str(third_lesson[k][2]) + ')']
            res_lessons.append(day_lessons)

    return res_lessons


all_lessons = concat_lesson(first_lesson_res, second_lesson_res, third_lesson_res)


class News:
    def __init__(self, title, categ_inf, url, cr_date):
        self.news_title = title
        self.news_url = url
        self.news_categ = categ_inf
        self.news_get_date = cr_date

    def __str__(self):
        return f'{self.news_title}\n{self.news_categ.lstrip().rstrip()}\n{self.news_url.lstrip()}\n{self.news_get_date}'


def take_news_to_list():
    url = 'https://www.rbc.ru/tags/?tag=%D0%9C%D0%B8%D0%BD%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D1%8B'
    result = requests.get(url)
    news_list = []
    soup = bs(result.text, 'html.parser')
    current_date = datetime.datetime.now()
    l_row_tag = soup.find('div', class_='l-row g-overflow js-search-container')

    dev_search_item_js_tag = l_row_tag.findAll('div', class_='search-item js-search-item')

    for item in dev_search_item_js_tag:
        item_title = item.find('span', class_='search-item__title').text
        item_category = item.find('span', class_='search-item__category').text
        item_url = item.a.get('href')
        new_news = News(item_title, item_category, item_url, current_date)
        news_list.append(new_news)

    return news_list


#TOKEN = os.environ['TOKEN']
TOKEN = os.environ.get('bot_token')
bot = telebot.TeleBot(TOKEN)
id_list = [1201776385, 629728192]


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
                if str(curr_date) == i[0]:
                    show_lesson_to_bot(i, call)

        elif call.data == 'tomorrow':
            for i in lessons:
                if str(tomorrow_date.date()) == i[0]:
                    show_lesson_to_bot(i, call)


@bot.message_handler(content_types=['text'])
def about_tex(message):
    bot.reply_to(message, f'Команда - "{message.text}" не предусмотрена программой данного бота')


bot.polling(none_stop=True)
current_date = datetime.datetime.now()
print(current_date)
