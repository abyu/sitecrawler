from crawler.link import Link

class LinkTagParser():
  def __init__(self, link_builder, no_op_builder):
    self.link_builder = link_builder
    self.no_op_builder = no_op_builder
  
  def parse(self, tag, attrs):
    attributes = self.validated_attributes(attrs)
    if(self.can_parse(tag) and attributes):
      return self.link_builder.create_new(attributes['href'])

    return self.no_op_builder

  def can_parse(self, tag):
    return tag == "a"

  def validated_attributes(self, attrs):
    attributes = dict(attrs)
    if 'href' in attributes:
      return attributes
    return None

  def reset(self):
    return self.no_op_builder

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

  def is_empty(self):
    return False

  def build(self):
    return Link(self.url, self.label, self.parent_url)

class NoOpBuilder:

  def create_new(self, url):
    return self

  def with_label(self, label):
    return self

  def build(self):
    return None

  def is_empty(self):
    return True
