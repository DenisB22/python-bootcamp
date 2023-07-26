import json

import requests
import bs4


# Function which get scrapes the New York Times website and creates a collection of all articles
def web_scraper(url: str) -> list:
    result = requests.get(url)

    soup = bs4.BeautifulSoup(result.text, 'lxml')

    story_wrapper = soup.select('.story-wrapper')
    articles_collection = []

    for story in story_wrapper:
        article_dict = {"title": "", "content": ""}

        title_list = story.select('h3')
        content_list = story.select('.summary-class')

        title = ''
        if title_list:
            title = title_list[0].getText()

        content = ''
        if content_list:
            content = content_list[0].getText()

        article_dict["title"] = title
        article_dict["content"] = content

        if title:
            articles_collection.append(article_dict)

    json_object = json.dumps(articles_collection, indent=4)

    # Export to JSON file
    with open('articles.json', 'w') as outfile:
        outfile.write(json_object)

    return articles_collection


if __name__ == "__main__":
    print(web_scraper('https://www.nytimes.com/'))