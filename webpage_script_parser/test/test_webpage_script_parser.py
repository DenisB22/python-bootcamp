from unittest import TestCase

from webpage_script_parser.webpage_script_parser import web_scraper


class WebPageScraperTests(TestCase):
    def test_incorrect_url_returns_empty_dict(self):
        url = 'https://www.google.com/'
        result = web_scraper(url)[0]
        self.assertEqual({}, result)

    def test_correct_url_return_articles_dict(self):
        url = 'https://www.nytimes.com/'
        result = web_scraper(url)[0]
        self.assertTrue(len(result) > 0)

    def test_response_status_200(self):
        url = 'https://www.nytimes.com/'
        response = str(web_scraper(url)[1])
        self.assertEqual('<Response [200]>', response)
