# import requests
import httpx
from bs4 import BeautifulSoup, Tag
from typing import List, Dict

class Scraper:
  def __init__(self, player_id: str):
    self.soup = None
    self.url = 'https://wank.wavu.wiki/player/'
    self.player_id = player_id
    self.char: str = ''
    self.content = None
    self.tables: Dict = {}
    
  def set_url(self) -> None:
    if not self.player_id:
      raise ValueError('Player_id not found')
    self.url = self.url + self.player_id
    if self.char:
      self.url = self.url + '/' + self.char
    
  def set_player_id(self, player_id: str) -> None:
    if not player_id:
      raise ValueError('Missing player id')
    self.player_id = player_id
    
  def set_char(self, char: str) -> None:
    if not char:
      raise ValueError('Missing character')
    self.char = char

  def set_tables(self) -> None:
    self.tables = self.soup.find_all('table')    
  
  def parse_page(self) -> None:
    if not self.content:
      raise Exception('No content to parse')
    try:
      self.soup = BeautifulSoup(self.content, 'html.parser')
    except Exception as e:
      print(f'Error while parsing page: {e}')
  
  async def get_page_content(self) -> None:
      if not self.url:
          raise ('No URL found')
      try:
          async with httpx.AsyncClient() as client:
              response = await client.get(self.url)
              if response.status_code == 200:
                  self.content = response.content
              else:
                  return None
      except Exception as e:
          print(f'Error while getting page: {e}')  
          
  def setup(self) -> None:
    self.parse_page()
    self.set_tables()
    return None
  
  def set_default_char(self) -> None:
    table = self.tables[2]
    body = table.find('tbody')
    tr = body.find('tr')
    char = tr.find_all('td')[0].text.strip()
    self.set_char(char)
    
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
  
  def get_head_to_head(self) -> List:
    if not self.tables:
      raise ValueError('No tables found')
    
    head_table = self.tables[4]
    heads = self.extract_rows(head_table)
    for head in heads:
      head[0] = head[0].strip("\n (h2h)")
    return heads
  

  def extract_rows(self, table: Tag, tbody: bool = True) -> List:
    """
    Extracts rows from a given HTML table.

    Args:
      table (Tag): The HTML table element to extract rows from.
      tbody (bool, optional): Specifies whether to look for rows within the 'tbody' element. 
                  Defaults to True.

    Returns:
      List: A list of lists, where each inner list represents a row in the table.
          The inner lists contain the text content of each cell in the row.

    """
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