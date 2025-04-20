from datetime import datetime
import json
import time
from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent, AgentEventLogger
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from auth.auth import get_current_user
from database.models import Meal, MealItem, User
from schema.user import UserCreate, UserLogin
from pathlib import Path
from database.dependency import get_db
from schema.llama import LlamaModel
import os
import re, json5

llama_router = APIRouter()

@llama_router.post("/chat")
# TODO: Add authenitcation
def chat(form_data: LlamaModel, db: Session = Depends(get_db), 
        #  user: User = Depends(get_current_user)
         ):
    
    user_meals = db.execute(
        select(MealItem)
        .join(Meal, Meal.id == MealItem.meal_id)
        .filter(Meal.user_id == 1)
    ).scalars().all()

    meal_dicts = [
        {
            "item_name": meal.item_name,
            "quantity": meal.quantity,
        }
        for meal in user_meals
    ] if user_meals else None
    
    instructions = """
        You are a nutrition assistant. A user will describe a meal they ate in natural language. Your job is to analyze each food item and return structured nutrition information.

        For each food item, return:
            name
            estimated quantity (e.g., '1 cup', '2 slices', '1 sandwich')
            calories (kcal)
            protein (g)
            carbohydrates (g)
            fat (g)
            The following micronutrients: iron, calcium, potassium, magnesium, zinc, sodium, vitamin A, vitamin C, vitamin D, vitamin B6, vitamin B12, fiber
        In addition to the food breakdown, use the current and past meals to provide a health analysis under a separate health_analysis field. Include:
            "summary": What trends or health patterns do you observe across the user's past meals? Use this data: {meal_dicts}.
            "new_meal_contribution": What does this particular meal add or fail to add? Does it improve any deficiencies or worsen any imbalances?
            "verdict": A short overall judgment of the meal's healthiness, possibly with friendly advice (e.g., "Great protein, but your fiber could use a boost. Maybe add a side salad next time.")
        
        Respond in a JSON format like below:
        {
        "meal_items": [
            {
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
            "summary": "",
            "new_meal_contribution": "",
            "verdict": ""
            },
            ...
        ]
        }
        Respond with valid JSON only (no trailing commas, no markdown, no extra text).
    """
    
    client = LlamaStackClient(base_url=f"http://localhost:8321")

    for _ in range(5):
        models = client.models.list()
        if models:
            break
        print("Waiting for models...")
        time.sleep(1)
    else:
        raise RuntimeError("No models available. Is Ollama running and the model loaded?")
    llm = models[1]
    
    model_id = llm.identifier
    vector_db_id = "nutrition-rag"
    agent = Agent(client, 
                  model=model_id, 
                  instructions=instructions,
                  tools=[
                        {
                            "name": "builtin::rag/knowledge_search",
                            "args": {"vector_db_ids": [vector_db_id]},
                    }
                ],
    )

    session_id = agent.create_session(session_name=f"s{uuid.uuid4().hex}")

    response = agent.create_turn(
        messages=[{"role": "user", "content": form_data.prompt}],
        session_id=session_id,
        stream=False,
    )
    
    raw = response.output_message.content
    raw = re.sub(r',\s*}', '}', raw)   # remove trailing comma before }
    raw = re.sub(r',\s*]', ']', raw)   # remove trailing comma before ]

    parsed = json.loads(response.output_message.content)

    # If LLM returned the list directly
    if isinstance(parsed, list):
        meal_items = parsed
    else:  # normal {"meal_items":[...]} shape
        meal_items = parsed.get("meal_items", [])

    if not meal_items:
        return {"response": response.output_message.content}

    # With this:
    new_meal = Meal(
        user_id=1,  # Replace with user.id when auth is added
        meal_type=form_data.meal_type,  # Use the meal_type from the request
        timestamp=datetime.utcnow()
    )
    db.add(new_meal)
    db.flush()  # Assigns ID so MealItem can reference new_meal.id
    
    print("HIDKFJLSDJF")

    # Add each meal item
    for item in meal_items:
        db_item = MealItem(
            meal_id=new_meal.id,
            item_name=item.get("name", ""),
            quantity=item.get("quantity", ""),
            calories=item.get("calories", 0),
            protein=item.get("protein", 0),
            carbohydrates=item.get("carbohydrates", 0),
            fat=item.get("fat", 0),
            fiber=item.get("fiber", 0),
            iron=item.get("iron", 0),
            calcium=item.get("calcium", 0),
            potassium=item.get("potassium", 0),
            magnesium=item.get("magnesium", 0),
            zinc=item.get("zinc", 0),
            sodium=item.get("sodium", 0),
            vitamin_a=item.get("vitamin A", 0),
            vitamin_c=item.get("vitamin C", 0),
            vitamin_d=item.get("vitamin D", 0),
            vitamin_b6=item.get("vitamin B6", 0),
            vitamin_b12=item.get("vitamin B12", 0),
        )
        db.add(db_item)

    db.commit()

    return {
        "response": response.output_message.content
    }