from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.link_tag_parser import LinkTagParser, LinkBuilder
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter
import logging

LOGGER = logging.getLogger("crawler.spider")

class Spider():

  def __init__(self, scraper, rules):
    self.scraper = scraper
    self.rules = rules

  def scrape(self, url, results_writer):
    scrape_results = self.__scrape_recursive(url, set())
    results_writer.write(scrape_results)
    return scrape_results

  def __scrape_recursive(self, url, scraped_urls):
    if url in scraped_urls:
      return None

    LOGGER.info("Scraping for link on page {0}".format(url))
    links = self.scraper.scrape_links(url)
    filtered_links = self.rules.apply_rules(links)

    LOGGER.info("Found {0} links, scrapping futher".format(len(filtered_links)))
    scraped_urls.add(url)
    child_links = list(map(lambda link: self.__scrape_recursive(link.get_url(), scraped_urls), filtered_links))
    LOGGER.info("Done scrapping {0}".format(url))

    return {"page_url": url, "child_links": [link for link in child_links if link]}

class LinkScraper():

  def __init__(self, http_client, html_parser):
    self.http_client = http_client
    self.html_parser = html_parser

  def scrape_links(self, url):
    tag_parser = self.get_tag_parser(url)
    page_content = self.http_client.get_html_page(url)
    if page_content:
      return self.html_parser.parse(tag_parser, page_content)
    return []

  def get_tag_parser(self, url):
    link_builder = LinkBuilder(url)

    return LinkTagParser(link_builder)
