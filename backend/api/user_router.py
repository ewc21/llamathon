import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from schema.user import UserCreate, UserLogin

from database.dependency import get_db
from database.models import Meal, MealItem, User

user_router = APIRouter()

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

meal_router = APIRouter()

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
