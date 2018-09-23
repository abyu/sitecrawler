from unittest import TestCase
from mock import patch, Mock
from crawler.http_client import HTTPClient

class HTTPClientTest(TestCase):

  @patch('requests.get')
  def test_get_html_page_for_given_url_only_for_ok_response_with_html_content(self, mock_get):
    mock_response = Mock()
    mock_response.text = "<html><body>Some html text</body></html>"
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_get.return_value = mock_response
    client = HTTPClient()
    page_content = client.get_html_page("http://www.something.com")

    self.assertEquals("<html><body>Some html text</body></html>", page_content)

  @patch('requests.get')
  def test_get_html_page_returns_nothing_for_a_non_ok_response(self, mock_get):
    mock_response = Mock()
    mock_response.text = "<html><body>Not found</body></html>"
    mock_response.status_code = 404
    mock_response.headers = {"Content-Type": "text/html"}
    mock_get.return_value = mock_response
    client = HTTPClient()
    page_content = client.get_html_page("http://www.something.com")

    self.assertIsNone(page_content)

  @patch('requests.get')
  def test_get_html_page_returns_nothing_for_a_non_html_content(self, mock_get):
    mock_response = Mock()
    mock_response.text = """{"some": "whatever"}"""
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_get.return_value = mock_response
    client = HTTPClient()
    page_content = client.get_html_page("http://www.something.com")

    self.assertIsNone(page_content)

  @patch('requests.get')
  def test_get_html_page_ignore_enconding_info_in_content_type(self, mock_get):
    mock_response = Mock()
    mock_response.text = "<html><body>Some html text</body></html>"
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "text/html; charset=UTF-8"}
    mock_get.return_value = mock_response
    client = HTTPClient()
    page_content = client.get_html_page("http://www.something.com")

    self.assertEquals("<html><body>Some html text</body></html>", page_content)