from typing import List, Dict
import pandas as pd

class Wavu:
  def __init__(self):
    self.tekken_id = str = None
    self.name = str = None
    self.region = str = None
    self.platform = str = None
    self.chars = List[str] = []
    self.current_char = str = ''
    self.ratings = List = []
    self.matches = List = []
    
  def set_ratings(self, ratings) -> None:
    self.ratings = ratings
    
  def set_matches(self, matches) -> None:
    self.matches = matches
    
  def set_current_char(self, char) -> None:
    self.current_char = char

  def get_total_games(self) -> int:
    if not self.ratings:
      raise ValueError('No ratings found')
    total_games = sum(int[row[3]] for row in self.ratings)
    return total_games
  
  def set_chars(self) -> None:
    if not self.ratings:
      raise ValueError('No ratings found')
    self.chars = [row[0] for row in self.ratings]
    self.current_char = self.chars[0]
  
  def get_chars(self) -> List[str]:
    return self.chars
  
  def get_total_results(self) -> Dict:
    wins = 0
    defeats = 0
    draws = 0
    for match in self.matches:
      result = match[1]
      if 'WIN' in result:
        wins += 1
      elif 'LOSE' in result:
        defeats += 1
      else:
        draws += 1

    total = wins + defeats + draws
    win_percentage = 0
    defeat_percentage = 0
    draw_percentage = 0
    
    if total != 0:
      win_percentage = (wins / total) * 100
      defeat_percentage = (defeats / total) * 100
      draw_percentage = (draws / total) * 100
      
    return {
      'wins': {'total': wins, 'percentage': "{:.2f}".format(win_percentage)},
      'defeats': {'total': defeats, 'percentage': "{:.2f}".format(defeat_percentage)},
      'draws': {'total': draws, 'percentage': "{:.2f}".format(draw_percentage)}}
    
  def get_total_chars(self) -> List:
    df = pd.DataFrame(self.matches, columns=['When', 'Score', 'Rating', 'Opponent', 'Opp. char', 'Opp. rating'])
    df = df.map(lambda x: x.strip())
    
    df['character'] = df['Opp. char'].str.extract(r'(\w+)')
    df['result'] = df['Score'].str.extract(r'(\w+)$')
    df[['rounds_won', 'rounds_lost']] =  df['Score'].str.extract(r'(\d+)-(\d+)').astype(int)
    
    results = df.pivot_table(index='character', columns='result', aggfunc='size', fill_value=0).reset_index()
    for col in results.columns[1:]:
      results[col] = results[col].astype(int)
    results['matches'] = results.iloc[:, 1:].sum(axis=1)
    
    rounds_won = df.groupby('character')['rounds_won'].sum().reset_index()
    rounds_lost = df.groupby('character')['rounds_lost'].sum().reset_index()

    results = pd.merge(results, rounds_won, on='character', how='left')
    results = pd.merge(results, rounds_lost, on='character', how='left')

    results.fillna(0, inplace=True)
    
    chars = results.to_json(orient='records')
    return chars