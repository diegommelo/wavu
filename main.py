from src.scraper import Scraper
from src.wavu import Wavu

test = Scraper()
player = Wavu()
test.set_url('https://wank.wavu.wiki/player/2FgyEG6H5NDr')
test.get_page_content()
test.parse_page()
ratings = test.get_ratings()
player.set_ratings(ratings)
print(player.get_total_games())