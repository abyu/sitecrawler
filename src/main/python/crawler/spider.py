from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter

class Spider():

  def __init__(self):
    pass

class LinkScraper():

  def __init__(self, http_client, html_parser):
    self.http_client = http_client
    self.html_parser = html_parser

  def scrape_links(self, url):
    page_content = self.http_client.get_html_page(url)
    if page_content:
      document = self.html_parser.parse(url, page_content)
      return document.get_links()
    return []


