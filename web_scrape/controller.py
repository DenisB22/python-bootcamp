from web_scrape.WebScraper import WebScraper

from web_scrape.logs.rotating_log import logger


# Controller which handles the creation of the first and second website
def controller() -> None:

    log_info = 'first website parameters attached, scraping is next'
    logger.info(log_info)

    web_scraper = WebScraper()

    # First Website
    first_website = web_scraper.web_scrape("https://bianchi.bg/kafe-na-zarna", ".product-thumb.product-wrapper .product-details",
                               ".product-thumb.product-wrapper .product-details .price",
                               ".product-thumb.product-wrapper .product-details .name",
                               ".product-thumb.product-wrapper .image .first-image", "data-src")

    # Extract the product with maximum and minimum price which will be sent to the function handling the export to CSV
    product_max = first_website[0]
    product_min = first_website[1]

    web_scraper.method_communicator(product_max, product_min)

    log_info = 'second website parameters attached, scraping is next'
    logger.info(log_info)

    web_scraper = WebScraper()

    # Second Website
    second_website = web_scraper.web_scrape(
        "https://kafemania.bg/kafe-na-zarna?gclid=Cj0KCQjwk96lBhDHARIsAEKO4xYMlLNaenK3FruhmrpfGt0fJIBuXfMY53CS9rYqGLmyrRXouN3rllcaAoOlEALw_wcB",
        ".product_grid__item .row.mx-n1.mx-sm-n2", ".product_grid__item .row.mx-n1.mx-sm-n2 .product_grid__price",
        ".product_grid__item .row.mx-n1.mx-sm-n2 .product_grid__name.js-home-new-products-title",
        ".row.mx-n1.mx-sm-n2 .col-6.col-sm-12.px-1.px-sm-2 .product_grid__image img", "data-src")

    # Extract the product with maximum and minimum price which will be sent to the function handling the export to CSV
    product_max = second_website[0]
    product_min = second_website[1]

    web_scraper.method_communicator(product_max, product_min)


if __name__ == '__main__':
    controller()