import logging
import multiprocessing as mp
from datetime import datetime
from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.link_tag_parser import LinkTagParser, LinkBuilder
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter
from crawler.parellel import ParellerRunner, TaskAction


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

  def scrape_parellel(self, url, results_writer, no_of_runners):
    pr = ParellerRunner(no_of_runners)
    pr.seed_input(url)
    pr.setup_workers(self.scrape_task)
    pr.setup_aggregator(self.aggregate_task, results_writer)
    pr.await_completion()

  def aggregate_task(self, task_item, in_queue, accumulator):
    if task_item == 'TERMINATE':
      return TaskAction.TERMINATE, accumulator

    visited_url = accumulator['visited_url']
    results = accumulator['results']
    link = task_item
    url = link.get_url()
    if not(url in visited_url):
      visited_url.add(url)
      results.append(link)
      in_queue.put(url)
    return TaskAction.CONTINUE, {'visited_url': visited_url, 'results': results}

  def scrape_task(self, url, out_queue):
    if url == 'TERMINATE':
      return TaskAction.TERMINATE

    LOGGER.info("Scraping for link on page {0}".format(url))
    links = self.scraper.scrape_links(url)
    filtered_links = self.rules.apply_rules(links)
    LOGGER.info("Found {0} links, scrapping futher".format(len(filtered_links)))
    for link in filtered_links:
        out_queue.put(link)

    return TaskAction.CONTINUE


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
