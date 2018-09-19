from unittest import TestCase
from crawler.urlfilter import SameDomainUrlFilter, DuplicateUrlFilter
from crawler.link import Link

class SameDomainUrlFilterTest(TestCase):

  def test_filter_url_based_on_given_domain(self):
    filter = SameDomainUrlFilter("http://google.com")
    link1InSameDomain = Link(url='/intl/de/policies/privacy/', label="Privacy", parent_url="http://google.com")
    link2InSameDomain = Link(url='/intl/de/policies/terms/', label="Terms", parent_url="http://google.com")
    linkInDifferentDomain = Link(url='http://www.youtube.com/?gl=DE&tab=w1', label="Video", parent_url="http://google.com")
    links = [
        link1InSameDomain,
        link2InSameDomain,
        linkInDifferentDomain
      ]

    filtered_links = filter.filter_links(links)

    self.assertEquals(2, len(filtered_links))
    self.assertCountEqual([link2InSameDomain, link1InSameDomain], filtered_links)

  def test_return_empty_when_no_urls_have_same_domain(self):
    filter = SameDomainUrlFilter("http://google.com")
    link1InDifferentDomain = Link(url='http://www.facebook.com', label="Terms", parent_url="http://google.com")
    link2InDifferentDomain = Link(url='http://www.youtube.com/?gl=DE&tab=w1', label="Video", parent_url="http://google.com")
    links = [
        link1InDifferentDomain,
        link2InDifferentDomain
      ]

    filtered_links = filter.filter_links(links)

    self.assertEquals(0, len(filtered_links))

class DuplicateUrlFilterTest(TestCase):

  def test_remove_urls_same_as_given_url(self):
    filter = DuplicateUrlFilter("http://google.com")
    linkRepeated1 = Link(url='http://google.com', label="Terms", parent_url="http://google.com")
    linkRepeated2 = Link(url='/', label="Video", parent_url="http://google.com")
    anotherLink = Link(url='http://www.facebook.com', label="Terms", parent_url="http://google.com")

    links = [
      linkRepeated1,
      linkRepeated2,
      anotherLink
    ]

    filtered_links = filter.filter_links(links)

    self.assertEquals(1, len(filtered_links))
    self.assertCountEqual([anotherLink], filtered_links)

  def test_return_empty_when_all_urls_are_duplicate(self):
    filter = DuplicateUrlFilter("http://google.com")
    linkRepeated1 = Link(url='http://google.com', label="Terms", parent_url="http://google.com")
    linkRepeated2 = Link(url='/', label="Video", parent_url="http://google.com")

    links = [
      linkRepeated1,
      linkRepeated2,
    ]

    filtered_links = filter.filter_links(links)

    self.assertEquals(0, len(filtered_links))

  def test_return_empty_when_for_empty_url_list(self):
    filter = DuplicateUrlFilter("http://google.com")
    links = []

    filtered_links = filter.filter_links(links)

    self.assertEquals(0, len(filtered_links))
