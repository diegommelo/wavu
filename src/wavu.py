from typing import List, Dict
import pandas as pd

class Wavu:
  def __init__(self):
    self.player_info: Dict = {}
    self.chars: List[str] = []
    self.current_char: str = ''
    self.ratings: List = []
    self.matches: List = []
    self.heads: List = []
    
  def set_ratings(self, ratings: List) -> None:
    self.ratings = ratings
    
  def set_matches(self, matches: List) -> None:
    self.matches = matches
    
  def set_current_char(self, char: List) -> None:
    self.current_char = char
    
  def set_player_info(self, info: List) -> None:
    self.player_info = info
    
  def set_chars(self) -> None:
    if not self.ratings:
      raise ValueError('No ratings found')
    self.chars = [row[0] for row in self.ratings]
    self.current_char = self.chars[0]
  
  def set_head_to_head(self, heads: List) -> None:
    self.heads = heads

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
    
  def get_total_chars(self) -> Dict:
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
    win_percentage = results['WIN'] / results['matches'] * 100
    results['win_percentage'] = win_percentage.round(2)
    rounds_won = df.groupby('character')['rounds_won'].sum().reset_index()
    rounds_lost = df.groupby('character')['rounds_lost'].sum().reset_index()
    
    results = pd.merge(results, rounds_won, on='character', how='left')
    results = pd.merge(results, rounds_lost, on='character', how='left')
    results.fillna(0, inplace=True)
    results = results.sort_values(by=['matches'], ascending=False)
    chars = results.to_dict(orient='records')
    return chars
  
  def get_player_info(self) -> Dict:
    if not self.player_info:
      return {}
    info = {
      'tekken_id': self.player_info[0][0],
      'region': self.player_info[2][0],
      'platform': self.player_info[3][0]
    }
    return info
  
  def get_top_head(self) -> List:
    """
    Returns the top 5 elements from the `heads` list.
    If the `heads` list is empty, it returns an empty list.

    Returns:
      List: The top 5 elements from the `heads` list.
    """
    if not self.heads:
      return []
    return self.heads[:5]
  
  def get_last_matches(self) -> List:
    if not self.matches:
      return {}
    last_matches = self.matches[:25]
    df = pd.DataFrame(last_matches, columns=['date', 'score', 'rating', 'opponent', 'opponent_char', 'opponent_rating'])
    columns_to_sanitize = ['rating', 'opponent', 'opponent_rating']
    for col in columns_to_sanitize:
      df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
      df[col] = df[col].str.replace(r'\n+', ' ', regex=True)
      df[col] = df[col].str.replace(r'\(h2h\)', ' ', regex=True)
      df[col] = df[col].str.strip()
    df['result'] = df['score'].str.extract(r'(\w+)$')
    df['score'] = df['score'].str.extract(r'(\d+-\d+)')
    df['rating'] = df['rating'].str.extract(r'(\d+\s+[+-]\d+)')
    # results = df.pivot_table(index='character', columns='result', aggfunc='size', fill_value=0).reset_index()
    # response = results.to_dict(orient='records')
    response = df.to_dict(orient='records')
    print(df)
    return response
