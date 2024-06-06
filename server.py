from fastapi import FastAPI, Query
from typing import Annotated
from src.scraper import Scraper
from src.wavu import Wavu

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
  
@app.get("/player/{player_id}")
async def get_player(player_id: str, char: Annotated[str | None, Query(min_length=3, max_length=10)] = None):
  if char:
    return {"player_id": player_id, "char": char}
  return {"player_id": player_id}