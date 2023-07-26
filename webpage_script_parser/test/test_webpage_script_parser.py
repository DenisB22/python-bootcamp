from unittest import TestCase

from webpage_script_parser.webpage_script_parser import web_scraper


class WebPageScraperTests(TestCase):
    def test_incorrect_url_returns_empty_dict(self):
        url = 'https://www.google.com/'
        result = web_scraper(url)
        self.assertEqual({}, result)

    def test_correct_url_return_articles_dict(self):
        url = 'https://www.nytimes.com/'
        result = web_scraper(url)
        self.assertTrue(len(result) > 0)

    # TODO: Test the response