import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from schema.user import UserCreate, UserLogin

from database.dependency import get_db
from database.models import Meal, MealItem, User
from schema.meal import MealCreate, MealItemCreate

user_router = APIRouter()
meal_router = APIRouter()

def calculate_calories(height: float, age: int, activity_level: str) -> int:
    base_calories = 10 * height + 6.25 * height - 5 * age + 5
    multiplier = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Very": 1.725,
    }[activity_level]
    return int(base_calories * multiplier)
    
@user_router.post("/login")
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = hash_password(user_data.password)
    new_user = User(username=user_data.username, 
                    hashed_password=hashed_pw, 
                    name=user_data.name, 
                    age = user_data.age, 
                    calories = calculate_calories(user_data.height, user_data.age, user_data.multiplier),
                    multiplier = user_data.multiplier)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "id": new_user.id}

@meal_router.get("/meals/{user_id}/{date}")
def get_meal_items_for_date(user_id: int, date: str, db: Session = Depends(get_db)):
    """
    Get all meal items for a given user and specific date (YYYY-MM-DD)
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Date must be in YYYY-MM-DD format")

    start = datetime.combine(date_obj, datetime.min.time())
    end = datetime.combine(date_obj, datetime.max.time())

    meal_items = (
        db.query(MealItem)
        .join(Meal)
        .filter(
            Meal.user_id == user_id,
            Meal.timestamp >= start,
            Meal.timestamp <= end
        )
        .all()
    )

    results = [{col.name: getattr(item, col.name) for col in item.__table__.columns} for item in meal_items]
    return {"meal_items": results}


@meal_router.post("/meal-items")
def add_meal_item(item: MealItemCreate, db: Session = Depends(get_db)):
    """
    Add a new meal item to a specific meal.
    """
    # Check if meal exists
    meal = db.query(Meal).filter(Meal.id == item.meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    new_item = MealItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "message": "Meal item added successfully",
        "meal_item_id": new_item.id,
        "item_name": new_item.item_name
    }
@meal_router.get("/meal-items/by-meal")
def get_meal_items_by_meal_ids(ids: list[int] = Query(...), db: Session = Depends(get_db)):
    items = db.query(MealItem).filter(MealItem.meal_id.in_(ids)).all()
    results = [{col.name: getattr(item, col.name) for col in item.__table__.columns} for item in items]
    return {"meal_items": results}

@meal_router.post("/meals/")
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db)):
    # Ensure the user exists
    user = db.query(User).filter(User.id == meal_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the meal
    new_meal = Meal(
        user_id=meal_data.user_id,
        meal_type=meal_data.meal_type
    )
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return {
        "message": "Meal created successfully",
        "meal_id": new_meal.id,
        "user_id": new_meal.user_id,
        "meal_type": new_meal.meal_type,
        "timestamp": new_meal.timestamp
    }
