from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

Response = [
  {
    "id": 1,
    "name": "Колонизаторы",
    "genre": "Стратегия",
    "players": 6
  },
  {
    "id": 2,
    "name": "Кодовые имена",
    "genre": "Пати-гейм",
    "players": 4
  }
]

app = FastAPI()

class Game(BaseModel):
    id: int
    name: str
    genre: str
    players: int

class POST_Game(BaseModel):
    name: str
    genre: str
    players: int

@app.get("/games", response_model=list[Game])
def getter():
    return Response

@app.post("/games", response_model=Game)
def postter(game: POST_Game):
    n_game = game.model_dump()
    n_game["id"] = len(Response) + 1
    
    Response.append(n_game)

    return n_game

@app.put("/games/{game_id}", response_model=Game)
def putter(game_id: int, game: POST_Game):
    for index, saved_games in enumerate(Response):
        if saved_games["id"] == game_id:
            u_game = game.model_dump()
            u_game["id"] = game_id

            Response[index] = u_game

            return u_game
    raise HTTPException(status_code=404, detail="Invalid ID")

@app.delete("/games/{game_id}", response_model=Game)
def deletter(game_id: int, game: POST_Game):
    for index, saves_games in enumerate(Response):
        if saves_games["id"] == game_id:
            d_game = Response.pop(index)

            return d_game
    raise HTTPException(status_code=404, detail="Invalid ID")
