import sys

from web_scrape.logs.rotating_log import logger

from skimage import io
import matplotlib.pyplot as plt


class Product:
    def __init__(self, name: str, price: float, image: str):
        self.name = name
        self.price = price
        self.image = image

    @staticmethod
    def show_image(url: str) -> None:
        log_info = 'visualize product images on desktop'
        logger.info(log_info)

        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True

        file = url
        a = io.imread(file)

        plt.imshow(a)
        plt.axis('off')

        plt.show()
