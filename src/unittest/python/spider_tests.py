from unittest import TestCase
from mockito import when, mock, unstub
from crawler.spider import Spider, LinkScraper
from crawler.link import Link

class SpiderTest(TestCase):

  def test_parse_all_links_in_page_for_the_given_url(self):
    pass

class LinkScraperTest(TestCase):
  def test_parse_all_links_in_page_for_the_given_url(self):
    page_url = "http://asamplepage.com"
    html_content = "An html page with links"
    page_links = [
      Link(url="/about", label="A link", parent_url="http://asamplepage.com"),
      Link("http://aurl.com", "A link", parent_url="http://asamplepage.com")
    ]
    mock_client = mock()
    mock_parser = mock()
    mock_document = mock()
    when(mock_client).get_html_page(page_url).thenReturn(html_content)
    when(mock_parser).parse(page_url, html_content).thenReturn(mock_document)
    when(mock_document).get_links().thenReturn(page_links)
    scraper = LinkScraper(mock_client, mock_parser)

    links = scraper.scrape_links(page_url)

    self.assertEquals(2, len(links))
    self.assertCountEqual(page_links, links)

  def test_parse_to_empty_links_when_the_url_does_not_return_a_html_page(self):
    page_url = "http://nonexistent.com"
    mock_client = mock()
    mock_parser = mock()
    mock_document = mock()
    when(mock_client).get_html_page(page_url).thenReturn(None)
    scraper = LinkScraper(mock_client, mock_parser)

    links = scraper.scrape_links(page_url)

    self.assertEquals(0, len(links))

