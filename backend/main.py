from fastapi import FastAPI, APIRouter, Depends
from starlette.middleware.cors import CORSMiddleware

from app.articles import article_router
from auth import login
from auth.login import validate_token
from db.db_connector import create_db_and_tables
from app.crud import crud_router
from app.tagger_api import tagger_router
from app.wikipedia import wiki_router
from app.websocket import websocket_router

app = FastAPI()

create_db_and_tables()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.login_router)
app.include_router(wiki_router)

apis = APIRouter(
    dependencies=[Depends(validate_token)],
)
apis.include_router(article_router)
apis.include_router(websocket_router)
app.include_router(crud_router)
app.include_router(tagger_router)

app.include_router(apis)