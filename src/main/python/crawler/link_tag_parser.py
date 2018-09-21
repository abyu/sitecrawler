from crawler.link import Link

class LinkTagParser():
  def __init__(self, link_builder):
    self.link_builder = link_builder
    self.current_builder = None
  
  def create_transaction(self, tag, attrs):
    if (not self.__transaction_exists()):
      attributes = self.__validated_attributes(attrs)
      if(self.can_parse(tag) and attributes):
        self.current_builder = self.link_builder.create_new(attributes['href'])

  def add_content(self, content):
    if self.__transaction_exists():
      self.current_builder.with_label(content)

  def commit(self, tag):
    if self.__transaction_exists():
      link = self.current_builder.build()
      self.current_builder = None
      return link
    return None

  def can_parse(self, tag):
    return tag == "a"

  def __validated_attributes(self, attrs):
    attributes = dict(attrs)
    if 'href' in attributes:
      return attributes
    return None

  def __transaction_exists(self):
    return self.current_builder

class LinkBuilder:

  def __init__(self, parent_url):
    self.url = ""
    self.label = ""
    self.parent_url = parent_url

  def create_new(self, url):
    self.url = url
    return self

  def with_label(self, label):
    self.label = label
    return self

  def build(self):
    return Link(self.url, self.label, self.parent_url)

