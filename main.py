from src.scraper import Scraper
from src.wavu import Wavu

test = Scraper()
player = Wavu()
test.set_url('https://wank.wavu.wiki/player/2FgyEG6H5NDr')
test.get_page_content()
test.parse_page()
test.set_tables()

ratings = test.get_ratings()
matches = test.get_matches()
player.set_matches(matches)
totals = player.get_total_results()
# print(totals)
# print(player.current_char)
# player.set_ratings(ratings)
# player.set_chars()
print (player.get_total_chars())