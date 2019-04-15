import requests
from bs4 import BeautifulSoup
import csv
import time
import random

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

root = 'https://www.idealista.com'
url = '/alquiler-viviendas/barcelona-provincia/'

refresh_cycle = 0
while url is not None:
    page = requests.get(root + url, headers=header)
    print(page.status_code)

    t = random.random()
    time.sleep(2 + t)

    if page.status_code != 200:
        with open('result.html', 'w') as result_page:
            result_page.write(page.text)

    soup = BeautifulSoup(page.content, features='html.parser')
    ads = [el for el in soup.find_all('article') if not el.has_attr('class')]

    t = random.random()
    time.sleep(2 + t)

    with open('data.csv', 'a+', newline='', encoding='utf-8') as data_file:
        csv_writer = csv.writer(data_file, delimiter=',')
        for ad in ads:
            name = ad.find_all(attrs={'class': 'item-link'})[0].string
            price = ad.find_all(attrs={'class': 'item-price'})[0].contents[0]
            currency = ad.find_all(attrs={'class': 'item-price'})[0].contents[1].string

            #  Property details
            details = ad.find_all(attrs={'class': 'item-detail'})
            if details is not None:
                n_rooms = details[0].contents[0]
            else:
                n_rooms = None

            if len(details) > 1:
                m_sq = details[1].contents[0]
            else:
                m_sq = None

            if len(details) > 2:
                house_type = details[2].text
            else:
                house_type = None

            csv_writer.writerow([name, price, currency, n_rooms, m_sq, house_type])

    next_button = soup.find('a', attrs={'class': 'icon-arrow-right-after'})
    if next_button is not None:
        url = next_button.get('href')
    else:
        url = None

    if refresh_cycle < 15:
        t = random.random()
        time.sleep(2 + 6*t)
        refresh_cycle += 1
    else:
        t = random.random()
        time.sleep(60 + 30 * t)
        refresh_cycle = 0
