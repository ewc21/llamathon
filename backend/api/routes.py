from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from auth.security import create_access_token, verify_password

from database.dependency import get_db
from database.models import User
# from api.chat_handler import handle_chat

user_router = APIRouter()

def calculate_calories(height: float, age: int, activity_level: str) -> int:
    base_calories = 10 * height + 6.25 * height - 5 * age + 5  # e.g., Mifflin-St Jeor
    multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
    }[activity_level]
    return int(base_calories * multiplier)

    
@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
