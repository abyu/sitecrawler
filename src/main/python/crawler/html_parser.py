from html.parser import HTMLParser
from crawler.link import Link
from crawler.link_tag_parser import LinkTagParser, LinkBuilder, NoOpBuilder
import logging

LOGGER = logging.getLogger("crawler.htmlparser")

class HtmlParser:
  
  def parse(self, parent_url, html_doc):
    doc = HTMLLinkParser(LinkTagParser(LinkBuilder(parent_url), NoOpBuilder()))
    doc.feed(html_doc)
    doc.close()
    return doc

class HTMLLinkParser(HTMLParser):

  def __init__(self, tag_parser):
    HTMLParser.__init__(self)
    self.tag_parser = tag_parser
    self.current_builder = tag_parser.reset()
    self.links = []

  def handle_starttag(self, tag, attrs):
    if self.current_builder.is_empty():
      self.current_builder = self.tag_parser.parse(tag, attrs)

  def handle_endtag(self, tag):
    item = self.current_builder.build()
    self.current_builder = self.tag_parser.reset()
    self.links.append(item) if item else None

  def handle_data(self, data):
    self.current_builder.with_label(data)
  
  def get_links(self):
    return self.links
