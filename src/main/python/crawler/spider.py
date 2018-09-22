from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.link_tag_parser import LinkTagParser, LinkBuilder
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter
import logging
import multiprocessing as mp
from datetime import datetime

LOGGER = logging.getLogger("crawler.spider")

class Spider():

  def __init__(self, scraper, rules):
    self.scraper = scraper
    self.rules = rules

  def scrape(self, url, results_writer):
    scrape_results = self.__scrape_recursive(url, set())
    results_writer.write(scrape_results)
    return scrape_results

  def aggregator(self, in_queue, out_queue, results_writer):
    visited_url = set()
    results = []
    while True:
      link = out_queue.get()
      if link == 'TERMINATE':
        LOGGER.info(list(visited_url))
        results_writer.write(results)
        return
      url = link.get_url()
      if not(url in visited_url):
        visited_url.add(url)
        results.append(link)
        in_queue.put(url)
      out_queue.task_done()

  def scrape_p(self, url, results_writer):
    m = mp.Manager()
    in_queue = m.JoinableQueue()
    out_queue = m.JoinableQueue()
    scrape_progress = m.JoinableQueue()
    in_queue.put(url)
    results = {}
    totalprocesors = 20
    processes = [mp.Process(target=self.scrape_worker, args=(in_queue, out_queue, scrape_progress )) for x in range(0, totalprocesors)]
    process_agg = mp.Process(target=self.aggregator, args=(in_queue, out_queue, results_writer, ))
    
    for process in processes:
      process.start()
    process_agg.start()

    while(True):
      in_queue.join()
      out_queue.join()
      LOGGER.info("Bothe ques empty {0}, {1}".format(out_queue.empty(), in_queue.empty()))
      LOGGER.info("Ongoing scrape? {0}".format(not scrape_progress.empty()))
      if(scrape_progress.empty()):
        break

    for x in range(0, totalprocesors):
      in_queue.put("TERMINATE")
    out_queue.put("TERMINATE")

    process_agg.join()
    for process in processes:
      process.join()
    
    return results
   
  def scrape_worker(self, in_queue, out_queue, scrape_progress):
    while True:
      url = in_queue.get(True)
      if url == 'TERMINATE':
        LOGGER.info("TERMINATING")
        in_queue.task_done()
        return
      LOGGER.info("Scraping for link on page {0}".format(url))
      scrape_progress.put("Scrape for {0}".format(url))
      links = self.scraper.scrape_links(url)
      filtered_links = self.rules.apply_rules(links)
      LOGGER.info("Found {0} links, scrapping futher".format(len(filtered_links)))
      for link in filtered_links:
        out_queue.put(link)
      scrape_progress.get()
      scrape_progress.task_done()
      in_queue.task_done()

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
