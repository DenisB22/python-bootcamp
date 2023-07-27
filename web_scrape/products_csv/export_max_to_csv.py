import pandas as pd
from datetime import datetime
import random

from web_scrape.logs.rotating_log import logger


# Function which checks if we already have a file, this will later be needed when we want to add data to the file
def export_only_cols_to_csv_max() -> bool:
    try:
        with open('./products_csv/products_max.csv', mode='r') as csvfile:

            log_info = 'checking if a CSV with maximum price statistics already exists'
            logger.info(log_info)

            return True

    except FileNotFoundError:
        return False


# When we already have a file, add only data rows, without generating new column headers
def export_only_rows_to_csv_max(product: dict) -> None:
    name = list(product.keys())[0]
    price = list(product.values())[0][0]
    image = list(product.values())[0][1]

    my_dict = {'id': [0], 'name': [name], 'price': [price], 'image': [image]}

    today = str(datetime.today())
    rand_num = random.randint(1, 10000)
    today_rand_num = today + str(rand_num)

    df = pd.DataFrame(my_dict)
    df['id'] = abs((df[['name']].sum(axis=1) + today_rand_num).map(hash))

    log_info = 'export only products with maximum price to CSV file'
    logger.info(log_info)

    df.to_csv('./products_csv/products_max.csv', mode='a', index=False, header=False)


# When we do not have a file, add data rows plus new column headers
def export_rows_and_cols_to_csv_max(product: dict) -> None:
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

    log_info = 'export column names and products with maximum price to CSV file'
    logger.info(log_info)

    df.to_csv("./products_csv/products_max.csv", index=False, columns=fields)
        

