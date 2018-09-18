from crawler.html_parser import LinkBuilder, NoOpBuilder
import unittest

class LinkBuilderTest(unittest.TestCase):

  def test_create_link_obj(self):
    lb = LinkBuilder()
    lb.create_new("http://aurl.com")
    link = lb.build()

    self.assertEquals({"url": "http://aurl.com", "label": ""}, link)

  def test_create_link_with_label(self):
    lb = LinkBuilder()
    link = lb.create_new("http://aurl.com").with_label("A Link")
    link = lb.build()

    self.assertEquals({"url": "http://aurl.com", "label": "A Link"}, link)

class NoOpBuilderTest(unittest.TestCase):

  def test_does_not_build_anything(self):
    nb = NoOpBuilder()
    item = nb.build()

    self.assertIsNone(item)
