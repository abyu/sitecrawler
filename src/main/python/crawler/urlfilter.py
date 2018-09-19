class SameDomainUrlFilter:

  def __init__(self, url):
    self.url = url

  def filter_links(self, links):
    filtered_links = list(filter(lambda link: link.is_same_domain(self.url), links))
    return filtered_links

class DuplicateUrlFilter:

  def __init__(self, url):
    self.url = url

  def filter_links(self, links):
    return list(filter(lambda link: not link.is_same_as(self.url), links))
