from api.routes import user_router as user_router
from fastapi import FastAPI
from llama_stack_client import LlamaStackClient

app = FastAPI()
client = LlamaStackClient()

app.include_router(user_router)