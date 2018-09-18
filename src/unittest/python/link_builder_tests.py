from crawler.html_parser import LinkBuilder, NoOpBuilder, Link
from unittest import TestCase

class LinkBuilderTest(TestCase):

  def test_create_link_obj(self):
    lb = LinkBuilder("")
    lb.create_new("http://aurl.com")
    link = lb.build()

    self.assertEquals(Link(url="http://aurl.com", label="", parent_url=""), link)

  def test_create_link_with_label(self):
    lb = LinkBuilder("")
    link = lb.create_new("http://aurl.com").with_label("A Link")
    link = lb.build()

    self.assertEquals(Link(url = "http://aurl.com", label="A Link", parent_url=""), link)

class NoOpBuilderTest(TestCase):

  def test_does_not_build_anything(self):
    nb = NoOpBuilder()
    item = nb.build()

    self.assertIsNone(item)

class LinkTest(TestCase):

  def test_links_with_same_urls_labels_parent_urls_are_equal(self):
    link = Link(url="http://thisurl.com", label="A link", parent_url="http://anotherlink.com")
    another_link = Link("http://thisurl.com", "A link", parent_url="http://anotherlink.com")

    self.assertEquals(another_link, link)

  def test_links_with_same_url_different_labels_are_unequal(self):
    link = Link("http://thisurl.com", "A link", parent_url="")
    another_link = Link("http://thisurl.com", "Something else", parent_url="")

    self.assertNotEqual(another_link, link)

  def test_link_is_not_equal_another_non_link_obj(self):
    link = Link("http://thisurl.com", "A link", parent_url="")

    self.assertNotEqual({"url": "somethig"}, link)

  def test_get_url_returns_the_url_string(self):
    link = Link("http://thisurl.com", "A link", parent_url="")

    url = link.get_url()

    self.assertEquals("http://thisurl.com", url)

  def test_get_url_returns_include_parent_url_for_a_relative_url(self):
    link = Link("/something", "A link", parent_url="www.apage.com")

    url = link.get_url()

    self.assertEquals("www.apage.com/something", url)
