from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import date
import time
import csv
import logging

logging.basicConfig(
    filename='log_Scraper.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

today_dirty = date.today()
d1 = today_dirty.strftime("%d/%m/%Y")
today2 = time.localtime()
current_time = time.strftime("%H:%M:%S", today2)
headers = {"User-Agent":
               "Mozilla/5.0 (Macintosh; "
               "Intel Mac OS X 10_15_7) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/101.0.4951.41 Safari/537.36"
           }


def scraper(url):
    pagecomputer = requests.get(url, headers=headers)

    soup1 = BeautifulSoup(pagecomputer.content, "html.parser")  # loading all HTML content to variable
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")  # making it look pretty, easier to read

    category_dirty = soup2.find("h1", {"class": "a-size-large a-spacing-medium a-text-bold"}).text
    category_semi_dirty = category_dirty.strip()
    category = category_semi_dirty[16:]
    print(category)

    product_name_computer_dirty = soup2.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"}).text
    product_name_computer = product_name_computer_dirty.strip()

    price_computer_dirty = soup2.find("span", {"class": "a-size-base a-color-price"}).text
    price_computer = price_computer_dirty.split()
    price = price_computer[1]

    rating_computer_dirty = soup2.find("span", {"class", "a-icon-alt"}).text
    rating_computer = rating_computer_dirty.strip()

    data = [category, product_name_computer, price, rating_computer, d1]

    with open('CSV/data_set_amazon.csv', 'a', encoding='UTF8') as file:
        row_writer = csv.writer(file)
        row_writer.writerow(data)


def top10mobile(url):
    page = requests.get(url, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    top_raw = soup2.find_all('span', {'class': 'zg-bdg-text'})
    product_raw = soup2.find_all('div', {'class': '_cDEzb_p13n-sc-css-line-clamp-3_g3dy1'})
    price_raw = soup2.find_all('span', {'class': '_cDEzb_p13n-sc-price_3mJ9Z'})
    print(price_raw)

    top_final = []  # formatting data from bs4 element to str
    top_list = []  # 1-20
    product_name_raw = []
    product_name_list = []  # clean product name data
    price_list_raw = []
    price_list = []
    wrapping = []
    score_list = []
    score_counter = 20

    # formatting data from bs4 element to str
    # defining top 20
    for i in range(20):
        top_final.append(top_raw[i])
        product_name_raw.append(product_raw[i])
        price_list_raw.append(price_raw[i])
        score_list.append(score_counter)
        score_counter -= 1

    # cleaning index data
    for index in top_final:
        r = index.get_text()
        rr = r.replace('#', '')
        rrr = rr.strip()
        top_list.append(rrr)

    # # cleaning product name
    for product_name in product_name_raw:
        t = product_name.get_text()
        tt = t.strip()
        product_name_list.append(tt)

    # cleaning price
    for price in price_list_raw:
        g = price.get_text()
        gg = g.split()
        price_list.append(gg[1])

    # creating list of lists to generate csv
    for v in range(20):
        wrapped = [top_list[v], score_list[v], product_name_list[v], price_list[v], d1, current_time]
        wrapping.append(wrapped)

    df = pd.DataFrame(wrapping)
    df.to_csv('/Users/fernandoiriarte/PycharmProjects/AmazonFirst/CSV/top20mobileV2.csv', mode='a', index=False,
              header=False)

    logging.info('ok')
    print('done')
