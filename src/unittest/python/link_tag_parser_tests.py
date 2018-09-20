from crawler.link_tag_parser import LinkBuilder, NoOpBuilder, LinkTagParser
from crawler.link import Link
from unittest import TestCase
from mockito import mock, when

class LinkTagParserTest(TestCase):
  def test_can_parse_anchor_tags(self):
    tag_parser = LinkTagParser(mock(), mock())

    can_parse = tag_parser.can_parse("a")

    self.assertTrue(can_parse)

  def test_cannot_parse_non_anchor_tags(self):
    tag_parser = LinkTagParser(mock(), mock())

    can_parse = tag_parser.can_parse("html")

    self.assertFalse(can_parse)

  def test_return_link_builder_for_anchor_tag_with_valid_attributes(self):
    mock_link_builder = mock()
    mock_no_op_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    tag_parser = LinkTagParser(mock_link_builder, mock_no_op_builder)
    
    builder = tag_parser.parse("a", [('href', '/about')])

    self.assertEquals(mock_link_builder, builder)

  def test_return_no_op_builder_for_non_anchor_tag(self):
    mock_link_builder = mock()
    mock_no_op_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder, mock_no_op_builder)
    
    builder = tag_parser.parse("span", [('id', '_about')])

    self.assertEquals(mock_no_op_builder, builder)

  def test_return_no_op_builder_for_an_anchor_tag_with_no_href_attribute(self):
    mock_link_builder = mock()
    mock_no_op_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder, mock_no_op_builder)
    
    builder = tag_parser.parse("a", [('class', '.sp-link')])

    self.assertEquals(mock_no_op_builder, builder)

  def test_return_no_op_builder_when_reset(self):
    mock_link_builder = mock()
    mock_no_op_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder, mock_no_op_builder)
    
    builder = tag_parser.reset()

    self.assertEquals(mock_no_op_builder, builder)


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

  def test_it_is_not_empty(self):
    lb = LinkBuilder("")
    
    is_empty = lb.is_empty()

    self.assertFalse(is_empty)

class NoOpBuilderTest(TestCase):

  def test_does_not_build_anything(self):
    nb = NoOpBuilder()

    item = nb.build()

    self.assertIsNone(item)

  def test_is_always_empty(self):
    nb = NoOpBuilder()
    
    is_empty = nb.is_empty()

    self.assertTrue(is_empty)

