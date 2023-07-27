import json

from web_scrape.logs.rotating_log import logger


def export_max_to_json(product_max: dict) -> None:

    for product_max_cur in product_max.items():

        product_max_name = product_max_cur[0]

        product_max_price = product_max_cur[1][0]
        product_max_image = product_max_cur[1][1]

        product_max_dict = {"Name": product_max_name, "Price": product_max_price,
                            "IMG": product_max_image}

        product_max_json = json.dumps(product_max_dict, indent=4)

        log_info = 'exporting product with max price to JSON file'
        logger.info(log_info)

        with open("./products_json/products_max.json", "w") as outfile:
            outfile.write(product_max_json)




