from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.db_connector import create_db_and_tables
from .auth import auth_router
from .crud import crud_router
from .wikipedia import wiki_router
from .websocket import websocket_router

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

app.include_router(auth_router)
app.include_router(wiki_router)
app.include_router(websocket_router)
app.include_router(crud_router)