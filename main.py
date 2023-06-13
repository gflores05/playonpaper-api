from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from connections.database import engine
from models import Base
from routers import games, players, match
from ws_routers import chat

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router)
app.include_router(players.router)
app.include_router(match.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    return {"message": "Play On Paper API"}
