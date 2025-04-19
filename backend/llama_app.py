from api.user_router import user_router
from api.llama_router import llama_router
from fastapi import FastAPI
from llama_stack_client import LlamaStackClient

from database.models import Base
from database.session import engine

app = FastAPI()
client = LlamaStackClient()

app.include_router(user_router)
app.include_router(llama_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)