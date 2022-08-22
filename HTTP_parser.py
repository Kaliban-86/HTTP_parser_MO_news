from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime
import pprint
import json

url = 'https://www.rbc.ru/tags/?tag=%D0%9C%D0%B8%D0%BD%D0%BE%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D1%8B'
result = requests.get(url)
print(result.status_code)
news_list = []
soup = bs(result.text, 'html.parser')
current_date = datetime.now()
l_row_tag = soup.find('div', class_='l-row g-overflow js-search-container')

dev_search_item_js_tag = l_row_tag.findAll('div', class_='search-item js-search-item')

# print(dev_search_item_js_tag)

for item in dev_search_item_js_tag:
    item_title = item.find('span', class_='search-item__title').text
    item_category = item.find('span', class_='search-item__category').text
    item_category_re = re.findall('\d{2} \w{3}, \d{2}:\d{2}', item_category)
    item_category_re_y = re.sub(r',', ' ' + str(current_date.year), item_category_re[0])
    item_to_app_to_list = f'{item_title} ({item_category_re_y})'

    news_list.append(item_to_app_to_list)
    print(item_to_app_to_list)
    print(item.a.get('href'))

# print(news_list)
# span_item_title_tag = l_row_tag.findAll('span', class_='search-item__title')
#
# spa_item_category_tag =
#
# for i in range(len(span_item_title_tag)):
#     pass
