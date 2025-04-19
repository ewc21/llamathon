from llama_stack import LlamaApp
from api.routes import router as api_router
from fastapi import FastAPI

app = FastAPI()
llama = LlamaApp(name="NutritionBot")

app.include_router(api_router)
