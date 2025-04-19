from api.routes import router as api_router
from fastapi import FastAPI
from llama_stack_client import LlamaStackClient

app = FastAPI()
client = LlamaStackClient()

app.include_router(api_router)
