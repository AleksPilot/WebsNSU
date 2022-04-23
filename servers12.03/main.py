from os import write
import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}

def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-items')
    for i in items:
        price = i.find('span', class_='d-inline-block').get_text()
        price = price.replace('р', '')
        name = i.find('h6', class_='card-title').get_text().strip()
        last_price = i.find('s', class_='d-inline-block').get_text().replace('р', '')
        discount = round((int(last_price) - int(price))/int(last_price)*100, 3)


        catalog.append({
            'name': name,
            'price': price,
            'last_price': last_price,
            'discount': discount
        })
    return catalog

def save_file(items, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Названия товара', 'Цена товара', 'Предыдущая цена', 'Скидка в процентах'])
        for item in items:
            writer.writerow([item['name'], item['price'], item['last_price'], item['discount']])



def parse():
    for URL in ['https://animeshop-akki.ru/manga/']:
        html = get_html(URL)
        if html.status_code == 200:
            html = get_content(html.text)
        else:
            print('Error')
        filename = 'parser.csv'
        save_file(html, filename)



parse()

