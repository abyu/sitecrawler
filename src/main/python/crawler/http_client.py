import requests

class HTTPClient:
  def get_html_page(self, url):
    response = requests.get(url)
    http_response = HTTPResponse(response)
    if(http_response.is_success() and http_response.is_html_content()):
      return http_response.content()
    return None

class HTTPResponse:

  def __init__(self, raw_response):
    self.raw_response = raw_response

  def is_success(self):
    return self.raw_response.status_code == 200

  def is_html_content(self):
    return "text/html" in self.__content_type()

  def __content_type(self):
    return self.raw_response.headers['Content-Type']

  def content(self):
    return self.raw_response.text