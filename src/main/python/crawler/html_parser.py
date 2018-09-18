from html.parser import HTMLParser

class HtmlParser:
  
  def parse(self, html_doc):
    doc = HTMLLinkParser(NoOpBuilder(), LinkBuilder())
    doc.feed(html_doc)
    doc.close()
    return doc

class HTMLLinkParser(HTMLParser):

  def __init__(self, no_op_builder, link_builder):
    HTMLParser.__init__(self)
    self.no_op_builder = no_op_builder
    self.link_builder = link_builder
    self.current_builder = no_op_builder
    self.links = []

  def handle_starttag(self, tag, attrs):
    #TODO: Move to builder factory
    if(tag == "a"):
      self.current_builder = self.link_builder.create_new(attrs[0][1])

  def handle_endtag(self, tag):
    item = self.current_builder.build()
    self.current_builder = self.no_op_builder
    self.links.append(item) if item else None

  def handle_data(self, data):
    self.current_builder.with_label(data)
  
  def get_links(self):
    return self.links

class LinkBuilder:

  def __init__(self):
    self.url = ""
    self.label = ""

  def create_new(self, url):
    self.url = url
    return self

  def with_label(self, label):
    self.label = label
    return self

  def build(self):
    return {"url": self.url, "label": self.label}

class NoOpBuilder:

  def create_new(self, url):
    return self

  def with_label(self, label):
    return self

  def build(self):
    return None
