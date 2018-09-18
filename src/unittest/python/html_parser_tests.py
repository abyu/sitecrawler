import unittest
from crawler.html_parser import HtmlParser, Link

class HtmlParserTest(unittest.TestCase):
  
  def test_parse_html_page_with_no_links_return_empty_list(self):
    html_parser = HtmlParser()
    parsed = html_parser.parse('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test</p></body></html>')
    links = parsed.get_links()

    self.assertEquals(0, len(links))

  def test_parse_a_link_in_html_page(self):
    html_parser = HtmlParser()
    parsed = html_parser.parse('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a href="http://somelink.com">SomeLink</a></p></body></html>')
    links = parsed.get_links()

    self.assertEquals(1, len(links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink"), links[0])

  def test_parse_multiple_links_in_html_page(self):
    html_parser = HtmlParser()
    parsed = html_parser.parse('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a href="http://somelink.com">SomeLink</a> and also <a href="http://anotherlink.com">AnotherLink</a></p></body></html>')
    links = parsed.get_links()

    self.assertEquals(2, len(links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink"), links[0])
    self.assertEquals(Link(url="http://anotherlink.com", label="AnotherLink"), links[1])

  def test_parse_multiple_links_on_different_levels_in_html_page(self):
    html_parser = HtmlParser()
    parsed = html_parser.parse("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
      <html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head>
        <body>
          <p>Some test<a href="http://somelink.com">SomeLink</a>
          and also <a target="_blank" href="http://anotherlink.com">AnotherLink</a></p>
          <div>
            <p>There is some text here with a link in another div
                <div><a href="http://adeeperlink.com">Deep</a></div>
            </p>
          </div>
        </body>
      </html>""")
    links = parsed.get_links()

    self.assertEquals(3, len(links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink"), links[0])
    self.assertEquals(Link(url="http://anotherlink.com", label="AnotherLink"), links[1])
    self.assertEquals(Link(url="http://adeeperlink.com", label="Deep"), links[2])
