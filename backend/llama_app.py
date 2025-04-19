from api.routes import user_router as user_router
from fastapi import FastAPI
from llama_stack_client import LlamaStackClient

from database.models import Base
from database.session import engine

app = FastAPI()
client = LlamaStackClient()

app.include_router(user_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)