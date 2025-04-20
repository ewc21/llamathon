from api.user_router import user_router
from api.llama_router import llama_router
from api.user_router import meal_router
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
    allow_origins=origins,  # only allow specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],     # allow all HTTP methods (POST, GET, etc)
    allow_headers=["*"],     # allow all headers including authorization
)

app.include_router(user_router)
app.include_router(meal_router)
app.include_router(llama_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)