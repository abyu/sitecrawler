from unittest import TestCase
from crawler.urlfilter import SameDomainUrlFilter
from crawler.html_parser import Link

class SameDomainUrlFilterTest(TestCase):

  def test_filter_url_based_on_given_domain(self):
    filter = SameDomainUrlFilter("http://google.com")

    links = [
        Link(url='/intl/de/policies/privacy/', label="Privacy", parent_url="http://google.com"),
        Link(url='/intl/de/policies/terms/', label="Terms", parent_url="http://google.com"),
        Link(url='http://www.youtube.com/?gl=DE&tab=w1', label="Video", parent_url="http://google.com")
      ]

    filtered_links = filter.filter_links(links)

    self.assertEquals(2, len(filtered_links))
