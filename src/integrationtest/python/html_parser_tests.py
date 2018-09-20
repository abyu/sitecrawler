import unittest
from crawler.html_parser import HtmlParser
from crawler.link_tag_parser import LinkTagParser, LinkBuilder, NoOpBuilder
from crawler.link import Link

parent_url = "http://parentlink.com"
links_parser = LinkTagParser(LinkBuilder(parent_url), NoOpBuilder())
html_parser = HtmlParser()

class HtmlParserTest(unittest.TestCase):

  def test_parse_html_page_with_no_links_return_empty_list(self):
    parsed_links = html_parser.parse(links_parser, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test</p></body></html>')

    self.assertEquals(0, len(parsed_links))

  def test_parse_a_link_in_html_page(self):
    parsed_links = html_parser.parse(links_parser, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a href="http://somelink.com">SomeLink</a></p></body></html>')

    self.assertEquals(1, len(parsed_links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink", parent_url=parent_url), parsed_links[0])

  def test_do_not_parse_a_link_with_no_href(self):
    parsed_links = html_parser.parse(links_parser, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a id="link">SomeLink</a></p></body></html>')

    self.assertEquals(0, len(parsed_links))

  def test_parse_a_link_in_html_page_containing_the_parent_url(self):
    parsed_links = html_parser.parse(links_parser, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a href="http://somelink.com">SomeLink</a></p></body></html>')

    self.assertEquals(1, len(parsed_links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink", parent_url=parent_url), parsed_links[0])

  def test_parse_a_link_ignoring_all_children_elements(self):
    parsed_links = html_parser.parse(links_parser, """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
      <html xmlns="http://www.w3.org/1999/xhtml">
        <head><title></title></head>
        <body>
          <p>Some test<a href="http://somelink.com"><span>SomeLink</span></a></p>
        </body>
      </html>""")

    self.assertEquals(1, len(parsed_links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink", parent_url=parent_url), parsed_links[0])

  def test_parse_multiple_links_in_html_page(self):
    parsed_links = html_parser.parse(links_parser, '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><p>Some test<a href="http://somelink.com">SomeLink</a> and also <a href="http://anotherlink.com">AnotherLink</a></p></body></html>')

    self.assertEquals(2, len(parsed_links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink", parent_url=parent_url), parsed_links[0])
    self.assertEquals(Link(url="http://anotherlink.com", label="AnotherLink", parent_url=parent_url), parsed_links[1])

  def test_parse_multiple_links_on_different_levels_in_html_page(self):
    parsed_links = html_parser.parse(links_parser, """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
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

    self.assertEquals(3, len(parsed_links))
    self.assertEquals(Link(url="http://somelink.com", label="SomeLink", parent_url=parent_url), parsed_links[0])
    self.assertEquals(Link(url="http://anotherlink.com", label="AnotherLink", parent_url=parent_url), parsed_links[1])
    self.assertEquals(Link(url="http://adeeperlink.com", label="Deep", parent_url=parent_url), parsed_links[2])

if __name__ == '__main__':
    unittest.main()