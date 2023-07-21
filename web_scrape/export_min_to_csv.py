import csv
import pandas as pd
from datetime import datetime
import random

# Function which checks if we already have a file, this will later be needed when we want to add data to the file
def export_only_cols_to_csv_min() -> bool:
    try:
        with open('products_min.csv', mode='r') as csvfile:
            return True

    except FileNotFoundError:
        return False


# When we already have a file, add only data rows, without generating new column headers
def export_only_rows_to_csv_min(product: dict) -> None:
    name = list(product.keys())[0]
    price = list(product.values())[0][0]
    image = list(product.values())[0][1]

    my_dict = {'id': [0], 'name': [name], 'price': [price], 'image': [image]}

    today = str(datetime.today())
    rand_num = random.randint(1, 10000)
    today_rand_num = today + str(rand_num)

    df = pd.DataFrame(my_dict)
    df['id'] = (df[['name']].sum(axis=1) + today_rand_num).map(hash)

    df.to_csv('products_min.csv', mode='a', index=False, header=False)


# When we do not have a file, add data rows plus new column headers
def export_rows_and_cols_to_csv_min(product: dict) -> None:
    name = list(product.keys())[0]
    price = list(product.values())[0][0]
    image = list(product.values())[0][1]

    my_dict = {'name': [name], 'price': [price], 'image': [image]}

    today = str(datetime.today())
    rand_num = random.randint(1, 10000)
    today_rand_num = today + str(rand_num)

    df = pd.DataFrame(my_dict)
    df['id'] = (df[['name']].sum(axis=1) + today_rand_num).map(hash)

    fields = ['id', 'name', 'price', 'image']

    df.to_csv("products_min.csv", index=False, columns=fields)


