import json

import requests
import bs4


# Function which get scrapes the New York Times website and creates a collection of all articles
def web_scraper(url: str) -> tuple:
    result = requests.get(url)

    soup = bs4.BeautifulSoup(result.text, 'lxml')

    # This should work!!!
    # article_headers = soup.select('.css-plkyuz')

    article_headers = soup.select('.css-9mylee h3')
    article_dict = {}

    counter = 0
    for article in article_headers:
        text = article.getText()

        if text:
            article_dict[counter] = text
            counter += 1

    # Create JSON object
    json_object = json.dumps(article_dict, indent=4)

    # Export to JSON file
    with open('articles.json', 'w') as outfile:
        outfile.write(json_object)

    return (article_dict, result)


if __name__ == "__main__":
    print(web_scraper('https://www.nytimes.com/'))