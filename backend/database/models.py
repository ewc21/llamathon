from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, JSON, Float, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    name = Column(String, nullable=False)
    height = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    multiplier = Column(Enum("Sedentary", "Light", "Moderate", "Very"), nullable=True)
    calories = Column(Integer, nullable=True)
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_type = Column(Enum("breakfast", "lunch", "dinner", "snacks", name="meal_type_enum"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # Use server default time

    # Relationships
    user = relationship("User", back_populates="meals")
    meal_items = relationship("MealItem", back_populates="meal", cascade="all, delete-orphan") # Cascade deletes


class MealItem(Base):
    __tablename__ = 'meal_items'

    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    item_name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)

    # Macronutrients
    calories = Column(Float, nullable=True, default=0.0)
    protein = Column(Float, nullable=True, default=0.0)
    carbohydrates = Column(Float, nullable=True, default=0.0)
    fat = Column(Float, nullable=True, default=0.0)
    fiber = Column(Float, nullable=True, default=0.0)

    # Micronutrients
    iron = Column(Float, nullable=True, default=0.0)
    calcium = Column(Float, nullable=True, default=0.0)
    potassium = Column(Float, nullable=True, default=0.0)
    magnesium = Column(Float, nullable=True, default=0.0)
    zinc = Column(Float, nullable=True, default=0.0)
    sodium = Column(Float, nullable=True, default=0.0)
    vitamin_a = Column(Float, nullable=True, default=0.0)
    vitamin_c = Column(Float, nullable=True, default=0.0)
    vitamin_d = Column(Float, nullable=True, default=0.0)
    vitamin_b6 = Column(Float, nullable=True, default=0.0)
    vitamin_b12 = Column(Float, nullable=True, default=0.0)

    # Relationship
    meal = relationship("Meal", back_populates="meal_items")
