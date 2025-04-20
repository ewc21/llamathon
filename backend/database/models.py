from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func # For default timestamp

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    name = Column(String, nullable=False)
    height = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    activity_level = Column(Enum("Sedentary", "Lightly Active", "Moderately Active", "Very Active"), nullable=True)
    calories = Column(Integer, nullable=True)
    
    meals = relationship("Meal", back_populates="user")

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
    item_name = Column(String)
    quantity = Column(String)
    # Store all nutrients as Floats, defaulting to 0.0 if not provided
    # Macronutrients
    calories = Column(Float, nullable=False, default=0.0)
    protein = Column(Float, nullable=False, default=0.0) # (g)
    carbohydrates = Column(Float, nullable=False, default=0.0) # (g)
    sugars = Column(Float, nullable=False, default=0.0) # (g, subset of carbs)
    fiber = Column(Float, nullable=False, default=0.0) # (g, subset of carbs)
    fat = Column(Float, nullable=False, default=0.0) # (g, total fat)
    saturated_fat = Column(Float, nullable=False, default=0.0) # (g)
    polyunsaturated_fat = Column(Float, nullable=False, default=0.0) # (g)
    monounsaturated_fat = Column(Float, nullable=False, default=0.0) # (g)
    trans_fat = Column(Float, nullable=False, default=0.0) # (g)

    # Micronutrients - Vitamins (consider units, mg or mcg)
    vitamin_a = Column(Float, nullable=False, default=0.0) # (e.g., IU or mcg RAE)
    vitamin_c = Column(Float, nullable=False, default=0.0) # (mg)
    vitamin_d = Column(Float, nullable=False, default=0.0) # (IU or mcg)
    vitamin_e = Column(Float, nullable=False, default=0.0) # (mg)
    vitamin_k = Column(Float, nullable=False, default=0.0) # (mcg)
    thiamin_b1 = Column(Float, nullable=False, default=0.0) # (mg)
    riboflavin_b2 = Column(Float, nullable=False, default=0.0) # (mg)
    niacin_b3 = Column(Float, nullable=False, default=0.0) # (mg)
    vitamin_b6 = Column(Float, nullable=False, default=0.0) # (mg)
    folate_b9 = Column(Float, nullable=False, default=0.0) # (mcg DFE)
    vitamin_b12 = Column(Float, nullable=False, default=0.0) # (mcg)
    pantothenic_acid_b5 = Column(Float, nullable=False, default=0.0) # (mg)

    # Micronutrients - Minerals (mg or mcg)
    calcium = Column(Float, nullable=False, default=0.0) # (mg)
    iron = Column(Float, nullable=False, default=0.0) # (mg)
    potassium = Column(Float, nullable=False, default=0.0) # (mg)
    sodium = Column(Float, nullable=False, default=0.0) # (mg)
    magnesium = Column(Float, nullable=False, default=0.0) # (mg)
    zinc = Column(Float, nullable=False, default=0.0) # (mg)
    copper = Column(Float, nullable=False, default=0.0) # (mg)
    selenium = Column(Float, nullable=False, default=0.0) # (mcg)
    phosphorus = Column(Float, nullable=False, default=0.0) # (mg)

    # Other
    cholesterol = Column(Float, nullable=False, default=0.0) # (mg)
    sugar_alcohols = Column(Float, nullable=False, default=0.0) # (g)
    caffeine = Column(Float, nullable=False, default=0.0) # (mg)
    alcohol = Column(Float, nullable=False, default=0.0) # (g)
    omega_3 = Column(Float, nullable=False, default=0.0) # (g or mg)
    omega_6 = Column(Float, nullable=False, default=0.0) # (g or mg)

    # Relationship
    meal = relationship("Meal", back_populates="meal_items")
