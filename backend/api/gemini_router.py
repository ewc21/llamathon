import os
import json
import re
import faiss
import numpy as np
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

from database.models import Meal, MealItem
from schema.user import LlamaModel
from database.dependency import get_db

# === SETUP ===
gemini_router = APIRouter()
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")  # Or gemini-2.0-flash if available
def clean_response_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    text= re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    return text

print("CWD:", os.getcwd())

# Load FAISS index and chunk store at startup
faiss_index = faiss.read_index("api/rag/food_index.faiss")
with open("api/rag/food_chunks.json", "r") as f:
    food_chunks = json.load(f)

@gemini_router.post("/chat")
def chat(form_data: LlamaModel, db: Session = Depends(get_db)):
    # === Step 1: Embed user prompt ===
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vec = embed_model.encode([form_data.prompt]).astype("float32")
    print("first test:")
    # === Step 2: Retrieve relevant chunks from FAISS ===
    k = 20  # top-k similar chunks
    _, indices = faiss_index.search(query_vec, k)
    retrieved_text = "\n".join([food_chunks[i] for i in indices[0]])
    print("second test")
    # === Step 3: Format prompt for Gemini ===
    prompt = f"""
You are a nutrition assistant. The user will describe a meal in natural language.
Your job is to analyze it and return structured nutrition information in JSON.

For each food item, return:
- name
- estimated quantity (e.g., "1 cup", "2 slices")
- calories
- protein
- carbohydrates
- fat
- fiber
- iron, calcium, potassium, magnesium, zinc, sodium
- vitamin A, C, D, B6, B12

Here is additional nutritional context you can reference:\n{retrieved_text}

User meal description:
{form_data.prompt}

Respond in this format (JSON only):
{{
  "meal_items": [
    {{
      "name": "chicken sandwich",
      "quantity": "1 sandwich",
      "calories": 430,
      "protein": 28,
      "carbohydrates": 35,
      "fat": 18,
      "fiber": 4,
      "iron": 2,
      "calcium": 60,
      "potassium": 300,
      "magnesium": 25,
      "zinc": 1.2,
      "sodium": 700,
      "vitamin A": 200,
      "vitamin C": 5,
      "vitamin D": 2,
      "vitamin B6": 0.3,
      "vitamin B12": 0.4
    }},
    ...
  ]
}}
If the input is ambiguous, make a reasonable guess. If you don't know any of the nutrients, put it as 0. Only output the JSON — no explanations or extra text.
"""

    response = model.generate_content(prompt)
    raw = response.text
    print("third test:", raw)
    # === Step 4: Parse response ===
    raw = clean_response_text(raw)
    print("fourth test:", raw)
    try:
        parsed = json.loads(raw)
        print("Mcdonalds")
    except Exception:
        print("Taco Bell")
        return {"error": "Failed to parse Gemini response", "raw_response": raw}

    meal_items = parsed.get("meal_items", [])
    print("Meal:", meal_items)
    # === Step 5: Store in DB ===
    new_meal = Meal(user_id=1, meal_type="lunch", timestamp=datetime.utcnow())
    db.add(new_meal)
    db.flush()

    for item in meal_items:
        db_item = MealItem(
            meal_id=new_meal.id,
            item_name=item.get("name", ""),
            quantity=item.get("quantity", ""),
            calories=item.get("calories", 0.0),
            protein=item.get("protein", 0.0),
            carbohydrates=item.get("carbohydrates", 0.0),
            fat=item.get("fat", 0.0),
            fiber=item.get("fiber", 0.0),
            iron=item.get("iron", 0.0),
            calcium=item.get("calcium", 0.0),
            potassium=item.get("potassium", 0.0),
            magnesium=item.get("magnesium", 0.0),
            zinc=item.get("zinc", 0.0),
            sodium=item.get("sodium", 0.0),
            vitamin_a=item.get("vitamin A", 0.0),
            vitamin_c=item.get("vitamin C", 0.0),
            vitamin_d=item.get("vitamin D", 0.0),
            vitamin_b6=item.get("vitamin B6", 0.0),
            vitamin_b12=item.get("vitamin B12", 0.0),
        )
        db.add(db_item)

    db.commit()

    return {"response": parsed}
