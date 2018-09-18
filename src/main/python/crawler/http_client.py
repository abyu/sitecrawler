import requests

class HTTPClient:
  def get_html_page(self, url):
    response = requests.get(url)
    content_type = response.headers['Content-Type']
    if(response.status_code == 200 and ("text/html" in content_type)):
      return response.text
    return None