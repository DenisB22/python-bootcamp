import json

from web_scrape.logs.rotating_log import logger


def export_min_to_json(product_min: dict) -> None:

    for product_min_cur in product_min.items():

        product_min_name = product_min_cur[0]

        product_min_price = product_min_cur[1][0]
        product_min_image = product_min_cur[1][1]

        product_min_dict = {"Name": product_min_name, "Price": product_min_price,
                            "IMG": product_min_image}

        product_min_json = json.dumps(product_min_dict, indent=4)

        log_info = 'exporting product with max price to JSON file'
        logger.info(log_info)

        with open("./products_json/products_min.json", "w") as outfile:
            outfile.write(product_min_json)





