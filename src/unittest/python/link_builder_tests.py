from crawler.html_parser import LinkBuilder, NoOpBuilder
from crawler.link import Link
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
