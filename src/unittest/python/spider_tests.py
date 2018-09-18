from unittest import TestCase
from crawler.spider import Spider

class SpiderTest(TestCase):

  def test_parse_all_links_in_page_for_the_given_url(self):
    spider = Spider()

