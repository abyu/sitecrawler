import unittest
from urllib.parse import urlparse
from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.writer import FileWriter
from crawler.spider import Spider, LinkScraper
from crawler.urlfilter import CrawlerRules, SameDomainUrlFilter, SameHierarcyUrlFilter
from datetime import datetime
from crawler.service import SpiderService
import logging
import os

LOGGER = logging.getLogger("crawler.spider_test")
class SpiderTest(unittest.TestCase):
  def ignore_test_scrape_url_write_results_to_a_file(self):
    url_to_scrape = "https://www.webscraper.io/test-sites/e-commerce/allinone"
    service = SpiderService()

    time_start = datetime.now().timestamp()
    results = service.scrape_url(url_to_scrape, "results")
    time_end = datetime.now().timestamp()

    LOGGER.info("Time taken to scrape: {0}".format(time_end - time_start))
    file_created = os.path.exists(results['results_file'])

    self.assertTrue(file_created)

  def ignore_test_scrape_url_write_results_to_a_file_parellel(self):
    url_to_scrape = "https://www.webscraper.io/test-sites/e-commerce/allinone"
    service = SpiderService()

    time_start = datetime.now().timestamp()
    results = service.scrape_url_parallel(url_to_scrape, "results", 10)
    time_end = datetime.now().timestamp()

    LOGGER.info("Time taken to scrape: {0}".format(time_end - time_start))
    file_created = os.path.exists(results)

    self.assertTrue(file_created)

if __name__ == '__main__':
    unittest.main()