from crawler.html_parser import LinkBuilder, NoOpBuilder, Link
import unittest

class LinkBuilderTest(unittest.TestCase):

  def test_create_link_obj(self):
    lb = LinkBuilder()
    lb.create_new("http://aurl.com")
    link = lb.build()

    self.assertEquals(Link(url="http://aurl.com", label=""), link)

  def test_create_link_with_label(self):
    lb = LinkBuilder()
    link = lb.create_new("http://aurl.com").with_label("A Link")
    link = lb.build()

    self.assertEquals(Link(url = "http://aurl.com", label="A Link"), link)

class NoOpBuilderTest(unittest.TestCase):

  def test_does_not_build_anything(self):
    nb = NoOpBuilder()
    item = nb.build()

    self.assertIsNone(item)

class LinkTest(unittest.TestCase):

  def test_links_with_same_urls_labels_are_equal(self):
    link = Link("http://thisurl.com", "A link")
    another_link = Link("http://thisurl.com", "A link")

    self.assertEquals(another_link, link)

  def test_links_with_same_url_different_labels_are_unequal(self):
    link = Link("http://thisurl.com", "A link")
    another_link = Link("http://thisurl.com", "Something else")

    self.assertNotEqual(another_link, link)

  def test_link_is_not_equal_another_non_link_obj(self):
    link = Link("http://thisurl.com", "A link")

    self.assertNotEqual({"url": "somethig"}, link)
