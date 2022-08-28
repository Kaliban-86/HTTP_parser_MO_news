import telebot
from HTTP_parser import take_news_to_list
import news_class

bot = telebot.TeleBot('5552347263:AAEPUnlfWotos-Lj_7_hUGOmxbZY4CCRXpE')


@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message,
                 f'Бот предназначен для побликации подборки новостей по теме "МО РФ" с новостоного портала РБК')


@bot.message_handler(commands=['all_news'])
def send_welcome(message):
    new_list = take_news_to_list()
    for one_news in reversed(new_list):
        bot.reply_to(message, f'{one_news.news_url}')


@bot.message_handler(commands=['ten_news'])
def send_welcome(message):
    new_list = take_news_to_list()
    for one_news in reversed(new_list[:10]):
        bot.reply_to(message, f'{one_news.news_url}')


@bot.message_handler(commands=['five_news'])
def send_welcome(message):
    new_list = take_news_to_list()
    for one_news in reversed(new_list[:5]):
        bot.reply_to(message, f'{one_news.news_url}')

@bot.message_handler(content_types=['text'])
def about_tex(message):
        bot.reply_to(message, f'Команда - "{message.text}" не предусмотрена программой данного бота')


bot.polling(none_stop=True)
