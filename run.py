#!/usr/bin/env python

import argparse
import os
from crawler.service import SpiderService
from datetime import datetime

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("url")
  parser.add_argument("runners")
  parser.add_argument("out_dir")
  args = parser.parse_args()
  url = args.url
  output_dir = args.out_dir
  runners = int(args.runners)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  return url, runners, output_dir

def start_up(url, runners, output_dir):
  print("Crawling for {0}, with {1} runners".format(url, runners))
  service = SpiderService()
  timestamp_start = int(datetime.now().timestamp())
  output_file = service.scrape_url_parallel(url, output_dir, runners)
  timestamp_end = int(datetime.now().timestamp())

  total_time = timestamp_end - timestamp_start

  print("Took {0} seconds to scrape {1}".format(total_time, url))
  print("Results at {0}".format(output_file))

if __name__ == '__main__':
  url, runners, output_dir = parse_arguments()
  start_up(url, runners, output_dir)