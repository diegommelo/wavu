from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Annotated
from src.scraper import Scraper
from src.wavu import Wavu

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
  
@app.get("/api/player/{player_id}")
async def get_player(scraper: Annotated[Scraper, Depends()], c: Annotated[str | None, Query(min_length=3, max_length=10)] = None):
  response = {}
  wavu = Wavu()
  if c:
    scraper.set_char(c)
  scraper.set_url()
  # await scraper.setup()
  await scraper.get_page_content()
  scraper.parse_page()
  scraper.set_tables()
  if not scraper.char:
    scraper.set_default_char()
  
  info = scraper.get_player_info()
  matches = scraper.get_matches()
  heads = scraper.get_head_to_head()
  ratings = scraper.get_ratings()

  wavu.set_player_info(info)
  wavu.set_matches(matches)
  wavu.set_head_to_head(heads)
  wavu.set_ratings(ratings)
  
  player_info = wavu.get_player_info()
  total_results = wavu.get_total_results()
  total_chars = wavu.get_total_chars()
  head_to_head = wavu.get_top_head()
  last_matches = wavu.get_last_matches()
  current_char = scraper.char
   
  response = {
    'current_char': current_char,
    'player_info': player_info,
    'opp_chars': total_chars,
    'results': total_results,
    'head_to_head': head_to_head,
    'last_matches': last_matches
  }
  return response
  # return scraper.content

