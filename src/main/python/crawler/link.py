from urllib.parse import urlparse

class Link:
  def __init__(self, url, label, parent_url):
    self.url = urlparse(url)
    self.label = label.strip()
    self.parent_url = urlparse(parent_url)

  def get_url(self):
    if (self.__is_absolute_url()):
      qualified_url = self.url.geturl()
    else:
      qualified_url = "{0}{1}".format(self._parent_base_url(), self.url.geturl())
    return qualified_url.strip('/')

  def is_same_domain(self, url):
    target_url = urlparse(url)
    this_url = urlparse(self.get_url())
    return this_url.hostname == target_url.hostname

  def has_same_parent(self, url):
    target_url = urlparse(url)
    this_url = urlparse(self.get_url())
    target_path_sections = set(target_url.path.split('/'))
    this_path_sections = set(this_url.path.split('/'))
    has_same_parent = this_path_sections & target_path_sections == target_path_sections
    return self.is_same_domain(url) and has_same_parent

  def is_same_as(self, url):
    target_url = urlparse(url)
    this_url = urlparse(self.get_url())
    return this_url.geturl() == target_url.geturl()

  def _parent_base_url(self):
    return "{0}://{1}".format(self.parent_url.scheme, self.parent_url.hostname)

  def __is_absolute_url(self):
    return self.url.netloc

  def __str__(self):
    return str(self.__dict__)

  def __repr__(self):
    return str({"url": self.get_url(), "label": self.label, "uri": self.url.geturl(), "parent": self.parent_url.geturl()})

  def __eq__(self, other):
    if isinstance(other, Link):
      return self.__dict__ == other.__dict__
    return False