import os

base = "."
folders = [
    f"{base}/prompts",
    f"{base}/api",
    f"{base}/database",
    f"{base}/ingestion",
    f"{base}/retrieval",
    f"{base}/utils",
    f"{base}/frontend"
]

files_with_contents = {
    f"{base}/llama_app.py": """from llama_stack import LlamaApp
from api.routes import router as api_router
from fastapi import FastAPI

app = FastAPI()
llama = LlamaApp(name="NutritionBot")

app.include_router(api_router)
""",

    f"{base}/api/routes.py": """from fastapi import APIRouter, Request
from api.chat_handler import handle_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    return await handle_chat(data["message"])
""",

    f"{base}/api/chat_handler.py": """from llama_stack import prompt

@prompt("parse_meal", template_file="prompts/parse_meal_items.txt")
async def parse_meal_items(user_input: str):
    return {"input": user_input}

async def handle_chat(user_input: str):
    structured = await parse_meal_items(user_input)
    return structured
""",

    f"{base}/prompts/parse_meal_items.txt": '''You are a nutrition assistant. Given a message from a user about what they ate, return a JSON list of meal items.

Example:
Input: I had a turkey sandwich and a Coke.
Output:
{
  "meal_items": [
    {"name": "turkey sandwich", "quantity": "1"},
    {"name": "Coke", "quantity": "1 can"}
  ]
}
''',

    f"{base}/database/models.py": '''from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime)

class MealItem(Base):
    __tablename__ = 'meal_items'
    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    item_name = Column(String)
    quantity = Column(String)
    macros = Column(JSON)
    micros = Column(JSON)
''',

    f"{base}/requirements.txt": '''fastapi
uvicorn
sqlalchemy
llama-stack
''',

    f"{base}/.env": "# Example: DB_URI=postgresql://user:pass@localhost/dbname\n"
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for filepath, content in files_with_contents.items():
    with open(filepath, "w") as f:
        f.write(content)

print(f"✅ {base} boilerplate generated!")
      