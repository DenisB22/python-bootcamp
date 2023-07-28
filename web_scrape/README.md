# Web Scraper Program
    A program that scrapes two online coffee stores. 
    After successfully completed scraping it exports 
    the Coffee Beans products with minimum and maximum
    prices from both websites to a CSV and JSON files.
    The program includes a CRON Job which can be set 
    to every "X" seconds/minutes/hours/days but can
    be also run on demand.

## Running the program

1. The program includes a controller which handles the starting of the script and the websites that will be scraped
   1. When the program needs to be run on demand, the user starts the controller.py module
2. When the CRON Job is needed, the programs needs to be run from the cron.py module
    1. The CRON Task is set to 15 minutes, which can be modified according to the needs of the user

## Program structure

1. The program includes log files, containing information about every step from the execution of the program
2. The program includes methods that are responsible for exporting data (image, minimum and maximum price of the products for the given page) to CSV and JSON files
3. The program includes "utils" folder, which contains the cron module and the module for visualizing the products on the user's screen
4. The controller.py module delegates the data to the WebScraper Object
5. The WebScraper Object 
   1. Collects and stores data for the products and finds the products with minimum and maximum prices
   2. Exports the products with maximum and minimum price to JSON files
   3. Exports the products with maximum and minimum price to CSV file
   4. Contains a method which is responsible for communicating with other methods