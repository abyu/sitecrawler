import logging

def initialize_logger():
  logging.basicConfig(filename="crawler.log", level=logging.INFO)

initialize_logger()
