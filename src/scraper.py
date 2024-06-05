import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict

class Scraper:
  def __init__(self):
    self.soup = None
    self.url: str = ''
    self.content = None
    self.tables: Dict = {}
    
  def set_url(self, url: str) -> None:
    if not url:
      raise Exception('No url found')
    self.url = url
    
  def get_page_content(self) -> None:
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
      
  def set_tables(self) -> None:
    self.tables = self.soup.find_all('table')
      
  def get_ratings(self) -> List:
    if not self.tables:
      raise ValueError('No tables found')
    
    ratings = []
    ratings_table = self.tables[2]
    ratings_body = ratings_table.find('tbody')
    rows = ratings_body.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      ratings.append([ele for ele in cols if ele])
    return ratings
  
  def get_matches(self) -> List:
    if not self.tables:
      raise ValueError('No tables found')
  
    matches_table = self.tables[3]
    matches = self.extract_rows(matches_table)
    return matches
  
  def get_player_info(self) -> List:
    if not self.tables:
      raise ValueError('No tables found')
    
    player_table = self.tables[0]
    info = self.extract_rows(player_table, False)
    return info
  
  def get_player_name(self) -> List:
    if not self.tables:
      raise ValueError('No tables found')
    
    name_table = self.tables[1]
    name = self.extract_rows(name_table, False)
    return name
    
  def extract_rows(self, table: Tag, tbody: bool = True) -> List:
    data = []
    if tbody:
      body = table.find('tbody')
      rows = body.find_all('tr')
    else:
      rows = table.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele])
    return data