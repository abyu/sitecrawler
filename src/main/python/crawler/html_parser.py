from html.parser import HTMLParser

class HtmlParser:
  
  def parse(self, html_doc):
    doc = HTMLLinkParser()
    doc.feed(html_doc)
    doc.close()
    return doc

class HTMLLinkParser(HTMLParser):

  def __init__(self):
    HTMLParser.__init__(self)
    self.link = {}
    self.links = []
    self.found_link=False

  def handle_starttag(self, tag, attrs):
    if(tag == "a"):
      self.found_link=True
      self.link["url"] = attrs[0][1]

  def handle_endtag(self, tag):
    if(self.found_link):
      self.links.append(self.link)
      self.link = {}
    self.found_link=False

  def handle_data(self, data):
    if(self.found_link):
      self.link["label"] = data
  
  def get_links(self):
    return self.links
