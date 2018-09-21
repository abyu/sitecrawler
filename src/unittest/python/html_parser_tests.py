import unittest
from crawler.html_parser import HtmlParser
from crawler.link import Link
from mockito import mock, verify, when, expect

class HtmlParserTest(unittest.TestCase):

  def test_parse_create_parse_transaction_on_given_tag_parser_on_tag_start(self):
    mock_tag_parser = mock()
    html_parser = HtmlParser()

    html_parser.parse(mock_tag_parser, '<html></html>')

    verify(mock_tag_parser).create_transaction('html', [])

  def test_parse_add_content_to_given_tag_parser_on_data(self):
    mock_tag_parser = mock()
    html_parser = HtmlParser()

    html_parser.parse(mock_tag_parser, '<html>Something</html>')

    verify(mock_tag_parser).add_content('Something')

  def test_parse_return_items_received_from_tag_parser_transaction_commits(self):
    mock_tag_parser = mock()
    html_parser = HtmlParser()
    created_element = {"aKey": "aValue"}
    when(mock_tag_parser).commit('html').thenReturn(created_element)

    tags = html_parser.parse(mock_tag_parser, '<html />')

    self.assertCountEqual([created_element], tags)

  def test_parse_ignore_nones_received_from_tag_parser_transaction_commits(self):
    mock_tag_parser = mock()
    html_parser = HtmlParser()
    when(mock_tag_parser).commit('html').thenReturn(None)

    tags = html_parser.parse(mock_tag_parser, '<html />')

    self.assertEqual(0, len(tags))
