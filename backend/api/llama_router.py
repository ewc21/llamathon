from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent, AgentEventLogger
from rich.pretty import pprint
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from schema.user import UserCreate, UserLogin
from pathlib import Path
from database.dependency import get_db
from schema.llama import LlamaModel

llama_router = APIRouter()

@llama_router.post("/chat")
# TODO: Add authenitcation
def chat(form_data: LlamaModel, db: Session = Depends(get_db)):
    client = LlamaStackClient(base_url=f"http://localhost:8321")

    models = client.models.list()
        
    # llm = next(m for m in models if m.type == "llm")
    llm = models[0]
    model_id = llm.identifier
    
    print(llm.dict())
    instructions = Path("backend/llama_stack_client/instructions.txt").read_text()
    agent = Agent(client, model=model_id, instructions= instructions)

    session_id = agent.create_session(session_name=f"s{uuid.uuid4().hex}")

    response = agent.create_turn(
        messages=[{"role": "user", "content": form_data.prompt}],
        session_id=session_id,
        stream=False,
    )
    print("agent>", response.output_message.content)
    if any(kw in form_data.prompt.lower() for kw in ["yes", "done", "that looks good", "i'm satisfied"]):
        print("✅ Great! I've added the nutrition breakdown of your meal to your dashboard.")

        # Ask Llama to output JSON of meal
        final_structured_response = agent.create_turn(
            messages=[
                {"role": "user", "content": "Please return the nutrition breakdown in JSON as instructed earlier."}
            ],
            session_id=session_id,
            stream=False,
        )

        # Parse the JSON result (ideally handle edge cases with try/except)
        import json
        try:
            parsed = json.loads(final_structured_response.output_message.content)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse nutrition data.")

        # Save to database (example assumes parsed['meal_items'] exists)
        from database.models import Meal, MealItem
        from datetime import datetime

        meal = Meal(user_id=form_data.user_id, timestamp=datetime.now())
        db.add(meal)
        db.flush()  # get meal.id before committing

        for item in parsed["meal_items"]:
            db_item = MealItem(
                meal_id=meal.id,
                item_name=item["name"],
                quantity=item.get("quantity"),
                macros={
                    "calories": item.get("calories"),
                    "protein": item.get("protein"),
                    "carbohydrates": item.get("carbohydrates"),
                    "fat": item.get("fat")
                },
                micros={
                    "fiber": item.get("fiber"),
                    "iron": item.get("iron"),
                    "calcium": item.get("calcium"),
                    "potassium": item.get("potassium"),
                    "magnesium": item.get("magnesium"),
                    "zinc": item.get("zinc"),
                    "sodium": item.get("sodium"),
                    "vitamin A": item.get("vitamin A"),
                    "vitamin C": item.get("vitamin C"),
                    "vitamin D": item.get("vitamin D"),
                    "vitamin B6": item.get("vitamin B6"),
                    "vitamin B12": item.get("vitamin B12")
                }
            )
            db.add(db_item)

        db.commit()

        return {
            "message": "Meal saved to database!",
            "structured_data": parsed
        }

    return {
        "message": "chat continued",
        "response": response.output_message.content
    }
    return {"response": response.output_message.content}