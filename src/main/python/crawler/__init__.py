import logging
import logging.config
import os
import sys

def initialize_logger():
  if os.path.exists('logging.conf'):
    logging.config.fileConfig('logging.conf')
  else:
    logging.basicConfig(filename='crawler.log', level=logging.DEBUG)

initialize_logger()
