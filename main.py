from src.scraper import Scraper
from src.wavu import Wavu

scraper = Scraper()
player = Wavu()
scraper.set_url('https://wank.wavu.wiki/player/2FgyEG6H5NDr')
scraper.get_page_content()
scraper.parse_page()
scraper.set_tables()

ratings = scraper.get_ratings()
matches = scraper.get_matches()
info = scraper.get_player_info()

player.set_player_info(info)
player.set_matches(matches)
player.set_ratings(ratings)
# player.set_chars()
totals = player.get_total_results()
total_chars = player.get_total_chars()

print(total_chars)