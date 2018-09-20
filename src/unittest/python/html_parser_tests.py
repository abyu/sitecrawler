import unittest
from crawler.html_parser import HtmlParser
from crawler.link import Link
from mockito import mock, verify, when, expect

class HtmlParserTest(unittest.TestCase):

  def test_reset_to_tag_parser_default_builder_on_start(self):
    mock_tag_parser = mock()
    html_parser = HtmlParser()
    when(mock_tag_parser).reset().thenReturn(mock(), mock())

    html_parser.parse(mock_tag_parser, '<html></html>')

    verify(mock_tag_parser, times=2).reset()

  def test_parse_call_given_tag_parser_on_tag_start(self):
    mock_tag_parser = mock()
    mock_no_op = mock()
    when(mock_no_op).is_empty().thenReturn(True)
    when(mock_tag_parser).parse('html', []).thenReturn(mock())
    expect(mock_tag_parser, times=2).reset().thenReturn(mock_no_op)
    html_parser = HtmlParser()

    html_parser.parse(mock_tag_parser, '<html></html>')

    verify(mock_tag_parser).parse('html', [])

  def test_parse_do_not_call_tag_parser_on_inner_tag_start_when_a_tag_parse_is_in_progress(self):
    mock_tag_parser = mock()
    mock_no_op = mock()
    mock_builder = mock()
    when(mock_builder).is_empty().thenReturn(False)
    when(mock_no_op).is_empty().thenReturn(True)
    when(mock_tag_parser).parse('html', []).thenReturn(mock())
    expect(mock_tag_parser, times=3).reset().thenReturn(mock_no_op)
    html_parser = HtmlParser()

    html_parser.parse(mock_tag_parser, '<html><body></body></html>')

    verify(mock_tag_parser).parse('html', [])

  def test_parse_reset_to_default_tag_builder_on_end_tag(self):
    mock_tag_parser = mock()
    mock_no_op = mock()
    mock_builder = mock()
    when(mock_no_op).is_empty().thenReturn(True)
    when(mock_tag_parser).parse('html', []).thenReturn(mock())
    expect(mock_tag_parser, times=2).reset().thenReturn(mock_no_op)
    html_parser = HtmlParser()

    html_parser.parse(mock_tag_parser, '<html />')

    verify(mock_tag_parser, times=2).reset()
