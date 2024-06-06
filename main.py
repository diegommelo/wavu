from src.scraper import Scraper
from src.wavu import Wavu

scraper = Scraper('2FgyEG6H5NDr')
player = Wavu()
scraper.set_url()
scraper.get_page_content()
scraper.parse_page()
scraper.set_tables()

ratings = scraper.get_ratings()
matches = scraper.get_matches()
info = scraper.get_player_info()
heads = scraper.get_head_to_head()

player.set_player_info(info)
player.set_matches(matches)
player.set_ratings(ratings)
player.set_head_to_head(heads)
player.set_chars()
totals = player.get_total_results()
total_chars = player.get_total_chars()
total_heads = player.get_top_head()
player_info = player.get_player_info()

print(total_chars)