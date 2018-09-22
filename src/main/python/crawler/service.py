from urllib.parse import urlparse
from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser
from crawler.writer import FileWriter
from crawler.spider import Spider, LinkScraper
from crawler.urlfilter import CrawlerRules, SameDomainUrlFilter, SameHierarcyUrlFilter
from datetime import datetime

class SpiderService():

  def scrape_url(self, url_to_scrape, output_dir):
    file_name = "{0}/{1}".format(output_dir, self.generate_file_name(url_to_scrape))
    writer = self.get_filter_writer(file_name)
    
    spider = self.get_spider(url_to_scrape)
    results = spider.scrape(url_to_scrape, writer)

    return {"results": results, "results_file": file_name}

  def scrape_url_parellel(self, url_to_scrape, output_dir):
    file_name = "{0}/{1}".format(output_dir, self.generate_file_name(url_to_scrape))
    writer = self.get_filter_writer(file_name)
    spider = self.get_spider(url_to_scrape)

    results = spider.scrape_parellel(url_to_scrape, writer)

    return file_name

  def get_spider(self, url_to_scrape):
    scraper = self.get_link_scraper()
    rules = self.get_crawler_rules(url_to_scrape)
    return Spider(scraper, rules)

  def get_http_client(self):
    return HTTPClient()

  def get_html_parser(self):
    return HtmlParser()

  def get_link_scraper(self):
    http_client = self.get_http_client()
    html_parser = self.get_html_parser()
    return LinkScraper(http_client, html_parser)

  def get_crawler_rules(self, url_to_scrape):
    same_domain_filter = SameDomainUrlFilter(url_to_scrape)
    same_hierarcy_filter = SameHierarcyUrlFilter(url_to_scrape)
    filters = [same_domain_filter, same_hierarcy_filter]

    return CrawlerRules(filters)

  def get_filter_writer(self, file_name):
    return FileWriter(file_name)

  def generate_file_name(self, url_to_scrape):
    url = urlparse(url_to_scrape)
    timestamp = int(datetime.now().timestamp() * 1000)
    return "{0}{1}_{2}".format(url.hostname.replace(".", "-"), url.path.replace("/", "_"), timestamp)