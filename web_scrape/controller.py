from web_scrape.products_csv.export_max_to_csv import export_only_cols_to_csv_max, export_only_rows_to_csv_max, \
    export_rows_and_cols_to_csv_max
from web_scrape.products_json.export_max_to_json import export_max_to_json
from web_scrape.products_csv.export_min_to_csv import export_only_rows_to_csv_min, export_rows_and_cols_to_csv_min
from web_scrape.products_json.export_min_to_json import export_min_to_json
from web_scrape.logs.rotating_log import logger
from web_scrape.web_scraper import web_scrape


# Communicator with CSV exporter module
def module_communicator(product_max: dict, product_min: dict) -> None:
    file_exists = export_only_cols_to_csv_max()

    if file_exists:
        # Call the functions which handle the adding of only rows, because we already have column headers
        export_only_rows_to_csv_max(product_max)
        export_only_rows_to_csv_min(product_min)
    else:
        # Call the functions which handle adding both the column headers and the information of the first product
        export_rows_and_cols_to_csv_max(product_max)
        export_rows_and_cols_to_csv_min(product_min)

    export_min_to_json(product_min)
    export_max_to_json(product_max)


# Controller which handles the creation of the first and second website
def controller() -> None:

    log_info = 'first website parameters attached, scraping is next'
    logger.info(log_info)

    # First Website
    first_website = web_scrape("https://bianchi.bg/kafe-na-zarna", ".product-thumb.product-wrapper .product-details",
                               ".product-thumb.product-wrapper .product-details .price",
                               ".product-thumb.product-wrapper .product-details .name",
                               ".product-thumb.product-wrapper .image .first-image", "data-src")

    # Extract the product with maximum and minimum price which will be sent to the function handling the export to CSV
    product_max = first_website[0]
    product_min = first_website[1]

    module_communicator(product_max, product_min)

    log_info = 'second website parameters attached, scraping is next'
    logger.info(log_info)

    # Second Website
    second_website = web_scrape(
        "https://kafemania.bg/kafe-na-zarna?gclid=Cj0KCQjwk96lBhDHARIsAEKO4xYMlLNaenK3FruhmrpfGt0fJIBuXfMY53CS9rYqGLmyrRXouN3rllcaAoOlEALw_wcB",
        ".product_grid__item .row.mx-n1.mx-sm-n2", ".product_grid__item .row.mx-n1.mx-sm-n2 .product_grid__price",
        ".product_grid__item .row.mx-n1.mx-sm-n2 .product_grid__name.js-home-new-products-title",
        ".row.mx-n1.mx-sm-n2 .col-6.col-sm-12.px-1.px-sm-2 .product_grid__image img", "data-src")

    # Extract the product with maximum and minimum price which will be sent to the function handling the export to CSV
    product_max = second_website[0]
    product_min = second_website[1]

    module_communicator(product_max, product_min)


if __name__ == '__main__':
    controller()