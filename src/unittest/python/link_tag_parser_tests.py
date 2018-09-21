from crawler.link_tag_parser import LinkBuilder, LinkTagParser
from crawler.link import Link
from unittest import TestCase
from mockito import mock, when, verify
from mockito.matchers import ANY

class LinkTagParserTest(TestCase):
  def test_can_parse_anchor_tags(self):
    tag_parser = LinkTagParser(mock())

    can_parse = tag_parser.can_parse("a")

    self.assertTrue(can_parse)

  def test_cannot_parse_non_anchor_tags(self):
    tag_parser = LinkTagParser(mock())

    can_parse = tag_parser.can_parse("html")

    self.assertFalse(can_parse)

  def test_create_transaction_creates_new_link_for_anchor_tag_with_valid_attributes(self):
    mock_link_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder)

    tag_parser.create_transaction("a", [('href', '/about')])

    verify(mock_link_builder).create_new("/about")

  def test_create_transaction_does_not_create_new_link_for_an_anchor_tag_with_no_href_attribute(self):
    mock_link_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder)

    tag_parser.create_transaction("a", [('class', '.sp-link')])

    verify(mock_link_builder, times=0).create_new(ANY)

  def test_create_transaction_does_not_create_new_link_for_non_anchor_tag(self):
    mock_link_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder)

    tag_parser.create_transaction("span", [('id', '_about')])

    verify(mock_link_builder, times=0).create_new(ANY)

  def test_create_transaction_does_not_create_new_link_when_a_transaction_exists(self):
    mock_link_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    tag_parser = LinkTagParser(mock_link_builder)

    tag_parser.create_transaction("a", [('href', '/about')])
    tag_parser.create_transaction("a", [('href', '/blog')])

    verify(mock_link_builder).create_new("/about")
    verify(mock_link_builder, times=0).create_new("/blog")

  def test_add_data_to_link_when_a_transaction_exists(self):
    mock_link_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    tag_parser = LinkTagParser(mock_link_builder)
    tag_parser.create_transaction("a", [('href', '/about')])
  
    tag_parser.add_content("About")

    verify(mock_link_builder).with_label("About")

  def test_do_not_add_data_to_link_when_no_transaction_exists(self):
    mock_link_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    tag_parser = LinkTagParser(mock_link_builder)

    tag_parser.add_content("About")

    verify(mock_link_builder, times = 0).with_label("About")

  def test_return_created_link_from_existing_transaction_on_commit(self):
    expected_link = Link(url="/about", label="About", parent_url="http://something.com")
    mock_link_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    when(mock_link_builder).build().thenReturn(expected_link)
    tag_parser = LinkTagParser(mock_link_builder)
    tag_parser.create_transaction("a", [('href', '/about')])

    link = tag_parser.commit("a")

    self.assertEquals(expected_link, link)

  def test_commit_returns_nothing_when_there_is_no_existing_transaction(self):
    mock_link_builder = mock()
    tag_parser = LinkTagParser(mock_link_builder)

    link = tag_parser.commit("a")

    self.assertIsNone(link)

  def test_commit_returns_nothing_when_called_the_second_after_a_transaction_commit(self):
    expected_link = Link(url="/about", label="About", parent_url="http://something.com")
    mock_link_builder = mock()
    when(mock_link_builder).create_new("/about").thenReturn(mock_link_builder)
    when(mock_link_builder).build().thenReturn(expected_link)
    tag_parser = LinkTagParser(mock_link_builder)
    tag_parser.create_transaction("a", [('href', '/about')])

    link = tag_parser.commit("a")
    link_second_call = tag_parser.commit("a")

    self.assertEquals(expected_link, link)
    self.assertIsNone(link_second_call)


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
