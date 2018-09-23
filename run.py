#!/usr/bin/env python

from crawler.service import SpiderService
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
args = parser.parse_args()
url = args.url
print("Crawling for {0}".format(url))
service = SpiderService()
timestamp_start = int(datetime.now().timestamp())
output_file = service.scrape_url_parellel(url, "results")
timestamp_end = int(datetime.now().timestamp())

total_time = timestamp_end - timestamp_start

print("Took {0} seconds to scrape {1}".format(total_time, url))
print("Results at {0}".format(output_file))