from skimage import io
import matplotlib.pyplot as plt

from web_scrape.rotating_log import create_rotating_log, logger


# Function for visualizing the product image
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