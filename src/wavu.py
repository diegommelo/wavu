from typing import List

class Wavu:
  def __init__(self):
    self.tekken_id = None
    self.name = None
    self.region = None
    self.platform = None
    self.chars = []
    self.ratings = List
    
  def set_ratings(self, ratings) -> None:
    self.ratings = ratings
    
  def get_total_games(self) -> int:
    if not self.ratings:
      raise Exception('No ratings found')
    total_games = 0
    for row in self.ratings:
      total_games += int(row[3])
    return total_games