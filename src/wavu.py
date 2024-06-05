from typing import List, Dict
import pandas as pd

class Wavu:
  def __init__(self):
    self.player_info: List[str] = []
    self.chars: List[str] = []
    self.current_char: str = ''
    self.ratings: List = []
    self.matches: List = []
    
  def set_ratings(self, ratings) -> None:
    self.ratings = ratings
    
  def set_matches(self, matches) -> None:
    self.matches = matches
    
  def set_current_char(self, char) -> None:
    self.current_char = char
    
  def set_player_info(self, info) -> None:
    self.info = info
    
  def set_chars(self) -> None:
    if not self.ratings:
      raise ValueError('No ratings found')
    self.chars = [row[0] for row in self.ratings]
    self.current_char = self.chars[0]

  def get_total_games(self) -> int:
    if not self.ratings:
      raise ValueError('No ratings found')
    total_games = sum(int[row[3]] for row in self.ratings)
    return total_games
  
  def get_chars(self) -> List[str]:
    return self.chars
  
  def get_total_results(self) -> Dict:
    if not self.matches:
      return {}
    wins, defeats, draws = 0, 0, 0
    for match in self.matches:
      result = match[1]
      if 'WIN' in result:
        wins += 1
      elif 'LOSE' in result:
        defeats += 1
      else:
        draws += 1
        
      total = wins + defeats + draws
      percentages = {
            'wins': wins / total * 100 if total else 0,
            'defeats': defeats / total * 100 if total else 0,
            'draws': draws / total * 100 if total else 0
        }
      return {key: {'total': value, 'percentage': "{:.2f}".format(percentage)} for key, value, percentage in zip(percentages.keys(), (wins, defeats, draws), percentages.values())}
    
  def get_total_chars(self) -> str:
    if not self.matches:
      return '[]'
    df = pd.DataFrame(self.matches, columns=['When', 'Score', 'Rating', 'Opponent', 'Opp. char', 'Opp. rating'])
    df['character'] = df['Opp. char'].str.extract(r'(\w+)')
    df['result'] = df['Score'].str.extract(r'(\w+)$')
    df[['rounds_won', 'rounds_lost']] =  df['Score'].str.extract(r'(\d+)-(\d+)').astype(int)
    results = df.pivot_table(index='character', columns='result', aggfunc='size', fill_value=0).reset_index()
    
    for col in ['WIN', 'LOSE', 'DRAW']:
        if col not in results.columns:
            results[col] = 0
    
    results['matches'] = results[['WIN', 'LOSE', 'DRAW']].sum(axis=1)
    
    rounds_won = df.groupby('character')['rounds_won'].sum().reset_index()
    rounds_lost = df.groupby('character')['rounds_lost'].sum().reset_index()
    
    results = pd.merge(results, rounds_won, on='character', how='left')
    results = pd.merge(results, rounds_lost, on='character', how='left')
    results.fillna(0, inplace=True)
    
    chars = results.to_json(orient='records')

    return chars
  
  def get_player_info(self) -> List:
    if not self.player_info:
      return '[]'
    return self.player_info