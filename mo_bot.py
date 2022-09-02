import telebot
from HTTP_parser import take_news_to_list
from telebot import types

with open('token.txt', 'r') as f:
    token = f.read()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Добро пожаловать, я телебот MO_RF, могу рассказать тебе последние новости МО РФ!')


@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Бот предназначен для побликации подборки новостей по теме "МО РФ" с новостоного портала РБК')


@bot.message_handler(commands=['news'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Все новости")
    item2 = types.KeyboardButton("10 последних новостей")
    item3 = types.KeyboardButton("5 последних новостей")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, 'Сколько показать новостей?', reply_markup=markup)





@bot.message_handler(commands=['ten_news'])
def send_welcome(message):
    new_list = take_news_to_list()
    for one_news in reversed(new_list[:10]):
        bot.reply_to(message, f'{one_news.news_title} {one_news.news_url}')


@bot.message_handler(commands=['five_news'])
def send_welcome(message):
    new_list = take_news_to_list()
    for one_news in reversed(new_list[:5]):
        bot.reply_to(message, f'{one_news.news_url}')


@bot.message_handler(content_types=['text'])
def about_tex(message):
    new_list = take_news_to_list()
    if message.text.strip() == 'Все новости':
        for one_news in reversed(new_list):
            bot.reply_to(message, f'{one_news.news_url}')
    elif message.text.strip() == '10 последних новостей':
        for one_news in reversed(new_list[:10]):
            bot.reply_to(message, f'{one_news.news_title} {one_news.news_url}')
    elif message.text.strip() == '5 последних новостей':
        for one_news in reversed(new_list[:5]):
            bot.reply_to(message, f'{one_news.news_title} {one_news.news_url}')
    else:
        bot.reply_to(message, f'Команда - "{message.text}" не предусмотрена программой данного бота')


bot.polling(none_stop=True)
