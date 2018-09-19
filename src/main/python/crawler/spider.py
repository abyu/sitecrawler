from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter

class Spider():

  def __init__(self, scraper, rules):
    self.scraper = scraper
    self.rules = rules

  def scrape(self, url):
    return self.__scrape_recursive(url, [])

  def __scrape_recursive(self, url, scraped_urls):
    if url in scraped_urls:
      return None
    links = self.scraper.scrape_links(url)
    filtered_links = self.rules.apply_rules(links)
    scraped_urls.append(url)
    child_links = list(map(lambda link: self.__scrape_recursive(link.get_url(), scraped_urls), filtered_links))

    return {"page_url": url, "child_links": [link for link in child_links if link]}

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


