from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .auth import auth_router
from .wikipedia import router
from .websocket import websocket_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)
app.include_router(websocket_router)