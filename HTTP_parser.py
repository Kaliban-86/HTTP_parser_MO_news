from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from news_class import News


def take_news_to_list():
    url = 'https://www.rbc.ru/tags/?tag=%D0%9C%D0%B8%D0%BD%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D1%8B'
    result = requests.get(url)
    news_list = []
    soup = bs(result.text, 'html.parser')
    current_date = datetime.now()
    l_row_tag = soup.find('div', class_='l-row g-overflow js-search-container')

    dev_search_item_js_tag = l_row_tag.findAll('div', class_='search-item js-search-item')

    for item in dev_search_item_js_tag:
        item_title = item.find('span', class_='search-item__title').text
        item_category = item.find('span', class_='search-item__category').text
        item_url = item.a.get('href')
        new_news = News(item_title, item_category, item_url, current_date)
        news_list.append(new_news)

    return news_list


if __name__ == '__main__':
    news_list = take_news_to_list()
    for i in range(len(news_list)):
        print(news_list[i])
        print('-' * 70)
#
# with open('news_list.data', 'wb') as f:
#    pickle.dump(news_list,f)
