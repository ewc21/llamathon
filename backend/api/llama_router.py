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
from database.models import Meal, MealItem, User # Import MealItem
from schema.user import UserCreate, UserLogin
from pathlib import Path
from database.dependency import get_db
from schema.llama import LlamaModel
import os
import json # Import json library
from datetime import datetime # Import datetime

llama_router = APIRouter()

# --- Helper function to safely get float from dict ---
def get_float(data: dict, key: str, default: float = 0.0) -> float:
    """Safely gets a float value from a dictionary, defaulting if key is missing or value is not convertible."""
    value = data.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
# --- End Helper ---


@llama_router.post("/chat")
# TODO: Add authenitcation
def chat(form_data: LlamaModel, db: Session = Depends(get_db), 
        #  user: User = Depends(get_current_user)
         ):
    current_user_id = 1
    user_meals = db.execute(
        select(Meal)
        .filter(Meal.user_id == current_user_id) # Use current_user_id
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
    
    instructions = f"""
        You are a nutrition assistant. A user will describe a meal they ate in natural language. Your job is to analyze each food item and return structured nutrition information.

        For each food item, return ALL of the following fields, defaulting to 0 if unknown:
            name (string)
            quantity (string, e.g., '1 cup', '100g')
            calories (float, kcal)
            protein (float, g)
            carbohydrates (float, g)
            sugars (float, g)
            fiber (float, g)
            fat (float, g)
            saturated_fat (float, g)
            polyunsaturated_fat (float, g)
            monounsaturated_fat (float, g)
            trans_fat (float, g)
            vitamin_a (float, mcg RAE or IU - specify unit if possible in quantity/name, otherwise assume mcg RAE)
            vitamin_c (float, mg)
            vitamin_d (float, mcg or IU)
            vitamin_e (float, mg)
            vitamin_k (float, mcg)
            thiamin_b1 (float, mg)
            riboflavin_b2 (float, mg)
            niacin_b3 (float, mg)
            vitamin_b6 (float, mg)
            folate_b9 (float, mcg DFE)
            vitamin_b12 (float, mcg)
            pantothenic_acid_b5 (float, mg)
            calcium (float, mg)
            iron (float, mg)
            potassium (float, mg)
            sodium (float, mg)
            magnesium (float, mg)
            zinc (float, mg)
            copper (float, mg)
            selenium (float, mcg)
            phosphorus (float, mg)
            cholesterol (float, mg)
            sugar_alcohols (float, g)
            caffeine (float, mg)
            alcohol (float, g)
            omega_3 (float, g or mg)
            omega_6 (float, g or mg)

        Respond ONLY with a JSON object containing a single key "meal_items" which is a list of the food items with their nutrition breakdown. Example:
        {{
          "meal_items": [
            {{
              "name": "Scrambled Eggs",
              "quantity": "2 large",
              "calories": 140.0, "protein": 12.0, "carbohydrates": 1.0, "sugars": 0.5, "fiber": 0.0,
              "fat": 10.0, "saturated_fat": 3.0, "polyunsaturated_fat": 2.0, "monounsaturated_fat": 4.0, "trans_fat": 0.0,
              "vitamin_a": 160.0, "vitamin_c": 0.0, "vitamin_d": 1.0, "vitamin_e": 1.0, "vitamin_k": 0.3,
              "thiamin_b1": 0.02, "riboflavin_b2": 0.3, "niacin_b3": 0.1, "vitamin_b6": 0.1, "folate_b9": 24.0, "vitamin_b12": 0.6, "pantothenic_acid_b5": 0.7,
              "calcium": 50.0, "iron": 1.2, "potassium": 140.0, "sodium": 140.0, "magnesium": 10.0, "zinc": 0.9, "copper": 0.03, "selenium": 30.0, "phosphorus": 180.0,
              "cholesterol": 370.0, "sugar_alcohols": 0.0, "caffeine": 0.0, "alcohol": 0.0, "omega_3": 0.1, "omega_6": 1.2
            }},
            {{
              "name": "Whole Wheat Toast",
              "quantity": "1 slice",
              "calories": 80.0, "protein": 4.0, "carbohydrates": 14.0, "sugars": 1.5, "fiber": 2.5,
              "fat": 1.0, "saturated_fat": 0.2, "polyunsaturated_fat": 0.3, "monounsaturated_fat": 0.2, "trans_fat": 0.0,
              "vitamin_a": 0.0, "vitamin_c": 0.0, "vitamin_d": 0.0, "vitamin_e": 0.2, "vitamin_k": 1.0,
              "thiamin_b1": 0.1, "riboflavin_b2": 0.05, "niacin_b3": 1.0, "vitamin_b6": 0.05, "folate_b9": 20.0, "vitamin_b12": 0.0, "pantothenic_acid_b5": 0.1,
              "calcium": 30.0, "iron": 1.0, "potassium": 60.0, "sodium": 150.0, "magnesium": 25.0, "zinc": 0.4, "copper": 0.05, "selenium": 10.0, "phosphorus": 70.0,
              "cholesterol": 0.0, "sugar_alcohols": 0.0, "caffeine": 0.0, "alcohol": 0.0, "omega_3": 0.02, "omega_6": 0.2
            }}
          ]
        }}

        If the input is ambiguous, make a reasonable guess. If the user's message doesn't make sense, return an empty list: {{"meal_items": []}}.
        Do not add any conversational text or explanations outside the JSON structure.
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
    llama_response_content = response.output_message.content
    print("Llama response content:", llama_response_content)

    # --- Parse the JSON result ---
    try:
        # Clean potential markdown code fences
        if llama_response_content.startswith("```json"):
            llama_response_content = llama_response_content[7:]
        if llama_response_content.endswith("```"):
            llama_response_content = llama_response_content[:-3]
        llama_response_content = llama_response_content.strip()

        parsed_data = json.loads(llama_response_content)
        if "meal_items" not in parsed_data or not isinstance(parsed_data["meal_items"], list):
             raise ValueError("Invalid JSON structure: 'meal_items' key missing or not a list.")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing Llama response: {e}")
        print(f"Raw response was: {llama_response_content}")
        raise HTTPException(status_code=500, detail=f"Failed to parse nutrition data from Llama. Error: {e}")

    # --- Save to database ---
    saved_items_data = []
    if parsed_data["meal_items"]: # Only proceed if Llama returned items
        try:
            # Create a single Meal entry for this log action
            # The meal_type needs to be passed from the frontend!
            # Add meal_type to LlamaModel schema and pass it from frontend handleLogSubmit
            meal = Meal(
                user_id=current_user_id, # Use current_user_id
                meal_type=form_data.meal_type, # Get from request data
                timestamp=datetime.now() # Or let DB handle default
            )
            db.add(meal)
            db.flush()  # Important: get the meal.id before creating items

            for item_data in parsed_data["meal_items"]:
                db_item = MealItem(
                    meal_id=meal.id,
                    item_name=item_data.get("name", "Unknown Item"),
                    quantity=item_data.get("quantity", ""),
                    # Map all fields using the helper function for safety
                    calories=get_float(item_data, "calories"),
                    protein=get_float(item_data, "protein"),
                    carbohydrates=get_float(item_data, "carbohydrates"),
                    sugars=get_float(item_data, "sugars"),
                    fiber=get_float(item_data, "fiber"),
                    fat=get_float(item_data, "fat"),
                    saturated_fat=get_float(item_data, "saturated_fat"),
                    polyunsaturated_fat=get_float(item_data, "polyunsaturated_fat"),
                    monounsaturated_fat=get_float(item_data, "monounsaturated_fat"),
                    trans_fat=get_float(item_data, "trans_fat"),
                    vitamin_a=get_float(item_data, "vitamin_a"),
                    vitamin_c=get_float(item_data, "vitamin_c"),
                    vitamin_d=get_float(item_data, "vitamin_d"),
                    vitamin_e=get_float(item_data, "vitamin_e"),
                    vitamin_k=get_float(item_data, "vitamin_k"),
                    thiamin_b1=get_float(item_data, "thiamin_b1"),
                    riboflavin_b2=get_float(item_data, "riboflavin_b2"),
                    niacin_b3=get_float(item_data, "niacin_b3"),
                    vitamin_b6=get_float(item_data, "vitamin_b6"),
                    folate_b9=get_float(item_data, "folate_b9"),
                    vitamin_b12=get_float(item_data, "vitamin_b12"),
                    pantothenic_acid_b5=get_float(item_data, "pantothenic_acid_b5"),
                    calcium=get_float(item_data, "calcium"),
                    iron=get_float(item_data, "iron"),
                    potassium=get_float(item_data, "potassium"),
                    sodium=get_float(item_data, "sodium"),
                    magnesium=get_float(item_data, "magnesium"),
                    zinc=get_float(item_data, "zinc"),
                    copper=get_float(item_data, "copper"),
                    selenium=get_float(item_data, "selenium"),
                    phosphorus=get_float(item_data, "phosphorus"),
                    cholesterol=get_float(item_data, "cholesterol"),
                    sugar_alcohols=get_float(item_data, "sugar_alcohols"),
                    caffeine=get_float(item_data, "caffeine"),
                    alcohol=get_float(item_data, "alcohol"),
                    omega_3=get_float(item_data, "omega_3"),
                    omega_6=get_float(item_data, "omega_6"),
                )
                db.add(db_item)
                # Prepare data to send back to frontend (optional but good practice)
                # Convert db_item back to a dict matching frontend expectations
                saved_item_dict = {f.name: getattr(db_item, f.name) for f in db_item.__table__.columns}
                saved_items_data.append(saved_item_dict)


            db.commit()
            print(f"Successfully saved {len(parsed_data['meal_items'])} items for meal {meal.id}")

        except Exception as e:
            db.rollback() # Rollback transaction on error
            print(f"Database Error: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save meal data to database. Error: {e}")

    # Return the data that was actually saved
    return {
        "message": f"Logged {len(saved_items_data)} items for {form_data.meal_type}.",
        "logged_items": saved_items_data # Send the saved items back
    }

    # --- Old return (replace with above) ---
    # return {
    #     "response": response.output_message.content # Don't just return raw llama response anymore
    # }