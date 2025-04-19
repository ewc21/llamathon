import time
from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent, AgentEventLogger
from rich.pretty import pprint
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from auth.auth import get_current_user
from database.models import Meal, User
from schema.user import UserCreate, UserLogin
from pathlib import Path
from database.dependency import get_db
from schema.llama import LlamaModel
import os

llama_router = APIRouter()

@llama_router.post("/chat")
# TODO: Add authenitcation
def chat(form_data: LlamaModel, db: Session = Depends(get_db), 
        #  user: User = Depends(get_current_user)
         ):
    
    user_meals = db.execute(
        select(Meal)
        # for testing
        # .filter(Meal.user_id == user.id)
        .filter(Meal.user_id == 1)
    ).scalars().all()

    meal_dicts = [
        {
            "item_name": meal.item_name,
            "quantity": meal.quantity,
            "macros": meal.macros,
            "micros": meal.micros,
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
            },
            ...
        ]
        }

        If the input is not a food item or a general question, you can avoid responding in the JSON format above and give an informative answer.
        If the input is ambiguous, make a reasonable guess. If the user's message doesn't make sense, seems impossible, or sounds like a joke, kindly point that out and ask them to clarify.
        Do not just repeat or accept nonsense. Be honest, informative, and a little witty if appropriate.
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
    print("agent>", response.output_message.content)
    # if any(kw in form_data.prompt.lower() for kw in ["yes", "done", "that looks good", "i'm satisfied"]):
    #     print("✅ Great! I've added the nutrition breakdown of your meal to your dashboard.")

    #     # Ask Llama to output JSON of meal
    #     final_structured_response = agent.create_turn(
    #         messages=[
    #             {"role": "user", "content": "Please return the nutrition breakdown in JSON as instructed earlier."}
    #         ],
    #         session_id=session_id,
    #         stream=False,
    #     )

    #     # Parse the JSON result (ideally handle edge cases with try/except)
    #     import json
    #     try:
    #         parsed = json.loads(final_structured_response.output_message.content)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail="Failed to parse nutrition data.")

    #     # Save to database (example assumes parsed['meal_items'] exists)
    #     from database.models import Meal, MealItem
    #     from datetime import datetime

    #     meal = Meal(user_id=form_data.user_id, timestamp=datetime.now())
    #     db.add(meal)
    #     db.flush()  # get meal.id before committing

    #     for item in parsed["meal_items"]:
    #         db_item = MealItem(
    #             meal_id=meal.id,
    #             item_name=item["name"],
    #             quantity=item.get("quantity"),
    #             macros={
    #                 "calories": item.get("calories"),
    #                 "protein": item.get("protein"),
    #                 "carbohydrates": item.get("carbohydrates"),
    #                 "fat": item.get("fat")
    #             },
    #             micros={
    #                 "fiber": item.get("fiber"),
    #                 "iron": item.get("iron"),
    #                 "calcium": item.get("calcium"),
    #                 "potassium": item.get("potassium"),
    #                 "magnesium": item.get("magnesium"),
    #                 "zinc": item.get("zinc"),
    #                 "sodium": item.get("sodium"),
    #                 "vitamin A": item.get("vitamin A"),
    #                 "vitamin C": item.get("vitamin C"),
    #                 "vitamin D": item.get("vitamin D"),
    #                 "vitamin B6": item.get("vitamin B6"),
    #                 "vitamin B12": item.get("vitamin B12")
    #             }
    #         )
    #         db.add(db_item)

    #     db.commit()

    #     return {
    #         "message": "Meal saved to database!",
    #         "structured_data": parsed
    #     }

    return {
        "response": response.output_message.content
    }