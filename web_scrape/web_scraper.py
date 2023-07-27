import requests
import bs4
import sys
import re

from Product import Product
from web_scrape.utils.vizualize import show_image


# Web scraping the given image and returning the products with maximum and minimum prices
def web_scrape(url: str, products_class: str, product_prices_class: str, product_names_class: str, product_images_class: str, image_src: str) -> tuple:
    min_price = sys.maxsize
    max_price = -sys.maxsize
    price_list = []
    products_collection = []

    result = requests.get(url)

    soup = bs4.BeautifulSoup(result.text, 'lxml')

    price_pattern = r"\d{1,2}.\d{1,2}"

    products = soup.select(products_class)

    product_prices = soup.select(product_prices_class)
    product_names = soup.select(product_names_class)
    product_images = soup.select(product_images_class)

    counter = 0

    log_info = 'web scraping starting, collecting products from web page'
    # logger = create_rotating_log('test.log')
    # logger.info(log_info)

    # Collect all products from the page
    for product in products:
        product_price = product_prices[counter]
        product_name = product_names[counter].getText()

        price = float(re.findall(price_pattern, product_price.text)[0])
        price_list.append(price)

        image = product_images[counter][image_src]

        product_cls = Product(product_name, price, image)
        products_collection.append(product_cls)

        counter += 1

    min_price = min(price_list)
    max_price = max(price_list)

    product_max_price = {x.name: [x.price, x.image] for x in products_collection if x.price == max(price_list)}
    product_min_price = {x.name: [x.price, x.image] for x in products_collection if x.price == min(price_list)}

    print(
        f"The Coffee Beans with the maximum price in the following Web Page is: {list(product_max_price.keys())[0]} with Price: {product_max_price[list(product_max_price.keys())[0]][0]}")
    show_image(product_max_price[list(product_max_price.keys())[0]][1])

    print(
        f"The Coffee Beans with the minimum price in the following Web Page is: {list(product_min_price.keys())[0]} with Price: {product_min_price[list(product_min_price.keys())[0]][0]}")
    show_image(product_min_price[list(product_min_price.keys())[0]][1])

    return (product_max_price, product_min_price)




