import requests
from bs4 import BeautifulSoup

class Scraper:
  def __init__(self):
    self.soup = None
    self.url = None
    self.content = None
    
  def set_url(self, url: str) -> None:
    if not url:
      raise Exception('No url found')
    self.url = url
    
  def get_page_content(self):
    if not self.url:
      raise ('No URL found')
    try:
      page = requests.get(self.url)
      if page.status_code == 200:
        self.content = page.content
      else:
        return None
    except Exception as e:
      print(f'Error while gettint page: {e}')
  
  def parse_page(self) -> None:
    if not self.content:
      raise Exception('No content to parse')
    try:
      self.soup = BeautifulSoup(self.content, 'html.parser')
    except Exception as e:
      print(f'Error while parsing page: {e}')
      
  def get_ratings(self):
    ratings = []
    tables = self.soup.find_all('table')
    ratings_table = tables[2]
    # ratings_header = ratings_table.find('thead')
    ratings_body = ratings_table.find('tbody')
    rows = ratings_body.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      ratings.append([ele for ele in cols if ele])
    return ratings