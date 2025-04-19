from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    name = Column(String, nullable=False)
    height = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    activity_level = Column(Enum("Sedentary", "Lightly Active", "Moderately Active", "Very Active"), nullable=False)
    calories = Column(Integer, nullable=False)

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
