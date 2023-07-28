import requests
import bs4
import sys
import re

from web_scrape.Product import Product
from web_scrape.logs.rotating_log import logger

import json

from web_scrape.logs.rotating_log import logger

import pandas as pd
from datetime import datetime
import random


class WebScraper:
    def __init__(self):
        self.products_collection = []
        self.price_list = []
        self.min_price = sys.maxsize
        self.max_price = -sys.maxsize

    def web_scrape(self, url: str, products_class: str, product_prices_class: str, product_names_class: str,
                   product_images_class: str, image_src: str) -> tuple:
        result = requests.get(url)

        soup = bs4.BeautifulSoup(result.text, 'lxml')

        price_pattern = r"\d{1,2}.\d{1,2}"

        products = soup.select(products_class)

        product_prices = soup.select(product_prices_class)
        product_names = soup.select(product_names_class)
        product_images = soup.select(product_images_class)

        counter = 0

        log_info = 'web scraping starting, collecting products from web page'
        logger.info(log_info)

        # Collect all products from the page
        for _ in products:
            product_price = product_prices[counter]
            product_name = product_names[counter].getText()

            price = float(re.findall(price_pattern, product_price.text)[0])
            # self.price_list.append(price)

            image = product_images[counter][image_src]

            product_cls = Product(product_name, price, image)

            self.price_list.append(price)

            self.products_collection.append(product_cls)

            counter += 1

        product_max_price = {x.name: [x.price, x.image] for x in self.products_collection
                             if x.price == max(self.price_list)}
        product_min_price = {x.name: [x.price, x.image] for x in self.products_collection
                             if x.price == min(self.price_list)}

        name_max = list(product_max_price.keys())[0]
        price_max = product_max_price[list(product_max_price.keys())[0]][0]
        image_max = product_max_price[list(product_max_price.keys())[0]][1]

        print(
            f"The Coffee Beans with the maximum price in the following Web Page is: "
            f"{name_max} with Price: "
            f"{price_max}")

        product_max = Product(name_max, price_max, image_max)
        image = product_max.image

        product_max.show_image(image)

        name_min = list(product_min_price.keys())[0]
        price_min = product_min_price[list(product_min_price.keys())[0]][0]
        image_min = product_min_price[list(product_min_price.keys())[0]][1]

        # print(product_min_price)
        print(
            f"The Coffee Beans with the minimum price in the following Web Page is: "
            f"{name_min} with Price: "
            f"{price_min}")

        product_min = Product(name_min,
                              price_min,
                              image_min)

        image = product_min.image

        product_min.show_image(image)

        return (product_max_price, product_min_price)

    @staticmethod
    def export_to_json(path, log_info, products):
        for product_cur in products.items():
            product_name = product_cur[0]

            product_price = product_cur[1][0]
            product_image = product_cur[1][1]

            product_dict = {"Name": product_name, "Price": product_price,
                            "IMG": product_image}

            product_json = json.dumps(product_dict, indent=4)

            logger.info(log_info)

            with open(path, "w") as outfile:
                outfile.write(product_json)

    @staticmethod
    def export_only_cols_to_csv(path, log_info) -> bool:
        try:
            with open(path, mode='r') as csvfile:

                logger.info(log_info)

                return True

        except FileNotFoundError:
            return False

    @staticmethod
    def export_only_rows_to_csv(path, log_info, product):
        name = list(product.keys())[0]
        price = list(product.values())[0][0]
        image = list(product.values())[0][1]

        my_dict = {'id': [0], 'name': [name], 'price': [price], 'image': [image]}

        today = str(datetime.today())
        rand_num = random.randint(1, 10000)
        today_rand_num = today + str(rand_num)

        df = pd.DataFrame(my_dict)
        df['id'] = abs((df[['name']].sum(axis=1) + today_rand_num).map(hash))

        logger.info(log_info)

        df.to_csv(path, mode='a', index=False, header=False)

    @staticmethod
    def export_rows_and_cols_to_csv(path, log_info, product: dict):
        name = list(product.keys())[0]
        price = list(product.values())[0][0]
        image = list(product.values())[0][1]

        my_dict = {'name': [name], 'price': [price], 'image': [image]}

        today = str(datetime.today())
        rand_num = random.randint(1, 10000)
        today_rand_num = today + str(rand_num)

        df = pd.DataFrame(my_dict)
        df['id'] = abs((df[['name']].sum(axis=1) + today_rand_num).map(hash))

        fields = ['id', 'name', 'price', 'image']

        logger.info(log_info)

        df.to_csv(path, index=False, columns=fields)

    def method_communicator(self, product_max: dict, product_min: dict) -> None:

        file_min_exists = self.export_only_cols_to_csv('./products_csv/products_min.csv',
                                                       'checking if a CSV with minimum price statistics already exists')

        if file_min_exists:
            self.export_only_rows_to_csv('./products_csv/products_min.csv',
                                         'export only products with minimum price to CSV file',
                                         product_min)
        else:
            self.export_rows_and_cols_to_csv("./products_csv/products_min.csv",
                                             'export column names and products with minimum price to CSV file',
                                             product_min)

        file_max_exists = self.export_only_cols_to_csv('./products_csv/products_max.csv',
                                                       'checking if a CSV with maximum price statistics already exists')

        if file_max_exists:
            self.export_only_rows_to_csv('./products_csv/products_max.csv',
                                         'export only products with maximum price to CSV file',
                                         product_max)
        else:
            self.export_rows_and_cols_to_csv("./products_csv/products_max.csv",
                                             'export column names and products with maximum price to CSV file',
                                             product_max)

        self.export_to_json('./products_json/products_min.json',
                            'exporting product with min price to JSON file',
                            product_min)
        self.export_to_json('./products_json/products_max.json',
                            'exporting product with max price to JSON file',
                            product_max)

