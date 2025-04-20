from pydantic import BaseModel
from typing import Optional, Literal

class MealItemCreate(BaseModel):
    meal_id: int
    item_name: str
    quantity: Optional[str] = None

    calories: float = 0.0
    protein: float = 0.0
    carbohydrates: float = 0.0
    sugars: float = 0.0
    fiber: float = 0.0
    fat: float = 0.0
    saturated_fat: float = 0.0
    polyunsaturated_fat: float = 0.0
    monounsaturated_fat: float = 0.0
    trans_fat: float = 0.0

    vitamin_a: float = 0.0
    vitamin_c: float = 0.0
    vitamin_d: float = 0.0
    vitamin_e: float = 0.0
    vitamin_k: float = 0.0
    thiamin_b1: float = 0.0
    riboflavin_b2: float = 0.0
    niacin_b3: float = 0.0
    vitamin_b6: float = 0.0
    folate_b9: float = 0.0
    vitamin_b12: float = 0.0
    pantothenic_acid_b5: float = 0.0

    calcium: float = 0.0
    iron: float = 0.0
    potassium: float = 0.0
    sodium: float = 0.0
    magnesium: float = 0.0
    zinc: float = 0.0
    copper: float = 0.0
    selenium: float = 0.0
    phosphorus: float = 0.0

    cholesterol: float = 0.0
    sugar_alcohols: float = 0.0
    caffeine: float = 0.0
    alcohol: float = 0.0
    omega_3: float = 0.0
    omega_6: float = 0.0
class MealCreate(BaseModel):
    user_id: int
    meal_type: Literal["breakfast", "lunch", "dinner", "snacks"]