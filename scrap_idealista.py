import requests
from bs4 import BeautifulSoup
import csv
import time
import random

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    'cookie': 'userUUID=f066086d-3bee-4d04-b43a-5533b797ca8b; _pxhd=f2722c368b8a7c659f888bff2bf2e0b8319383ac2ce01a1dfcb78284d550a9e3:2738eba0-4c05-11e9-9f03-954b7f911b10; xtvrn=$352991$; xtan352991=2-anonymous; xtant352991=1; cookieDirectiveClosed=true; _pxvid=2738eba0-4c05-11e9-9f03-954b7f911b10; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%22e0f63e0e-4825-4ba1-880f-204c329a37cd%22%2C%22options%22%3A%7B%22end%22%3A%222020-04-21T17%3A14%3A24.761Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-582065-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; optimizelyEndUserId=oeu1553188464829r0.7399545779228034; cto_lwid=0f5675b7-e51d-4d40-a9e0-0eb02c81cc91; listingGalleryBoostEnabled=false; detailFakeAnchorsEffect=true; SESSION=b4adfb56-66b3-4959-8df4-f6072644da71; cookieSearch-1="/venta-viviendas/sevilla-provincia/:1555317547313"; WID=c08d7f5cd41fbac0|XLRDL|XLRBU; utag_main=v_id:0169a13f267d000362c536bbec0303073003d06b00bd0$_sn:3$_ss:0$_st:1555319350273$ses_id:1555317076452%3Bexp-session$_pn:5%3Bexp-session; _pxff_tm=1; _px2=eyJ1IjoiZjA4NTU5ZjAtNWY1OS0xMWU5LWE4NWEtZTlkMmY5MmNhNDgxIiwidiI6IjI3MzhlYmEwLTRjMDUtMTFlOS05ZjAzLTk1NGI3ZjkxMWIxMCIsInQiOjE1NTUzMTc4NDg4MzksImgiOiJhYjQxYTI3MjNiNWFlNmViMjQxYWQ4YjA3M2NiNmI0ODZiN2E5NTZkMDdkNjg0MmI5NTE2OTkxZTQ4MjA3YThmIn0=',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

root = 'https://www.idealista.com'
url = '/https://www.idealista.com/alquiler-viviendas/barcelona-provincia/'
# url = 'https://www.idealista.com/venta-viviendas/sevilla-provincia/mapa'
# url = 'https://www.idealista.com/venta-viviendas/sevilla-provincia/'

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
