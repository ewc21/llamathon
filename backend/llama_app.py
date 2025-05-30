from api.user_router import user_router, meal_router 
from api.gemini_router import gemini_router
from fastapi import APIRouter, Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_stack_client import LlamaStackClient

from database.models import Base
from database.session import engine

app = FastAPI()
client = LlamaStackClient()

# Allow Vite frontend on localhost:5173
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # only allow specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods (POST, GET, etc)
    allow_headers=["*"],     # allow all headers including authorization
)

app.include_router(user_router)
app.include_router(gemini_router)
app.include_router(meal_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)