from skimage import io
import matplotlib.pyplot as plt


def show_image(url: str) -> None:
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    file = url
    a = io.imread(file)

    plt.imshow(a)
    plt.axis('off')

    plt.show()