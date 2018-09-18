from crawler.http_client import HTTPClient
from crawler.html_parser import HtmlParser

class Spider():

  def get_all_links(self, url):
    client = HTTPClient()
    parser = HtmlParser()

    page_content = client.get_html_page(url)
    if page_content:
      doc = parser.parse(page_content)
      return doc.get_links()
    return None