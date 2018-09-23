#!/usr/bin/env python

from crawler.service import SpiderService
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("runners")
args = parser.parse_args()
url = args.url
runners = int(args.runners)
print("Crawling for {0}, with {1} runners".format(url, runners))
service = SpiderService()
timestamp_start = int(datetime.now().timestamp())
output_file = service.scrape_url_parellel(url, "results", runners)
timestamp_end = int(datetime.now().timestamp())

total_time = timestamp_end - timestamp_start

print("Took {0} seconds to scrape {1}".format(total_time, url))
print("Results at {0}".format(output_file))