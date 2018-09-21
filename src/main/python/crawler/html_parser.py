from html.parser import HTMLParser
from crawler.link import Link
from crawler.link_tag_parser import LinkTagParser, LinkBuilder
import logging

LOGGER = logging.getLogger("crawler.htmlparser")

class HtmlParser:
  class _HTMLParser(HTMLParser):

    def __init__(self, tag_parser):
      HTMLParser.__init__(self)
      self.tag_parser = tag_parser
      self.tags = []

    def handle_starttag(self, tag, attrs):
      self.tag_parser.create_transaction(tag, attrs)

    def handle_endtag(self, tag):
      item = self.tag_parser.commit(tag)
      self.tags.append(item) if item else None

    def handle_data(self, data):
      self.tag_parser.add_content(data)

    def get_tags(self):
      return self.tags

  def parse(self, tag_parser, html_doc):
    doc = self._HTMLParser(tag_parser)
    doc.feed(html_doc)
    doc.close()
    return doc.get_tags()