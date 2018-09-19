from unittest import TestCase
from mockito import when, mock, unstub
from mockito.matchers import neq, ANY
from crawler.spider import Spider, LinkScraper
from crawler.link import Link

class SpiderTest(TestCase):

  def test_scrape_all_links_from_all_pages_in_same_domain_for_given_start_url(self):
    link_scraper = mock()
    crawler_rules = mock()
    when(link_scraper).scrape_links("http://samplepage.com").thenReturn([Link(url="/about", label="About", parent_url="http://samplepage.com")])
    when(link_scraper).scrape_links("http://samplepage.com/about").thenReturn([])
    when(crawler_rules).apply_rules([Link(url="/about", label="About", parent_url="http://samplepage.com")]).thenReturn([Link(url="/about", label="About", parent_url="http://samplepage.com")])
    when(crawler_rules).apply_rules([]).thenReturn([])
    spider = Spider(link_scraper, crawler_rules)
    links = spider.scrape("http://samplepage.com")
    expected_links = {
      "page_url": "http://samplepage.com",
      "child_links": [
        {
          "page_url": "http://samplepage.com/about",
          "child_links": []
        }
      ]
    }

    self.assertEquals(expected_links, links)

  def test_scrape_ignores_links_that_fail_the_rules(self):
    link_scraper = mock()
    crawler_rules = mock()
    same_domain_links1 = [Link(url="/about", label="About", parent_url="http://samplepage.com")]
    when(link_scraper).scrape_links("http://samplepage.com").thenReturn(same_domain_links1)
    when(link_scraper).scrape_links("http://samplepage.com/about").thenReturn([Link(url="http://anotherdoamin.com", label="External", parent_url="http://samplepage.com/about")])
    when(link_scraper).scrape_links("http://anotherdoamin.com").thenReturn([Link(url="/anotherabout", label="External About", parent_url="http://anotherdoamin.com")])
    when(link_scraper).scrape_links("http://anotherdoamin.com/anotherabout").thenReturn([])
    when(crawler_rules).apply_rules(same_domain_links1).thenReturn(same_domain_links1)
    when(crawler_rules).apply_rules(neq(same_domain_links1)).thenReturn([])

    spider = Spider(link_scraper, crawler_rules)
    links = spider.scrape("http://samplepage.com")
    expected_links = {
      "page_url": "http://samplepage.com",
      "child_links": [
        {
          "page_url": "http://samplepage.com/about",
          "child_links": []
        }
      ]
    }

    self.assertEquals(expected_links, links)

  def test_scrape_do_not_scrape_same_url_again(self):
    link_scraper = mock()
    crawler_rules = mock()
    same_domain_links1 = [Link(url="/about", label="About", parent_url="http://samplepage.com")]
    same_domain_links_repeated = [Link(url="http://samplepage.com", label="Home", parent_url="http://samplepage.com/about")]
    when(link_scraper).scrape_links("http://samplepage.com").thenReturn(same_domain_links1)
    when(link_scraper).scrape_links("http://samplepage.com/about").thenReturn(same_domain_links_repeated)
    when(crawler_rules).apply_rules(same_domain_links1).thenReturn(same_domain_links1)
    when(crawler_rules).apply_rules(same_domain_links_repeated).thenReturn(same_domain_links_repeated)
    spider = Spider(link_scraper, crawler_rules)
    links = spider.scrape("http://samplepage.com")
    expected_links = {
      "page_url": "http://samplepage.com",
      "child_links": [
        {
          "page_url": "http://samplepage.com/about",
          "child_links": []
        }
      ]
    }

    self.assertEquals(expected_links, links)

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

