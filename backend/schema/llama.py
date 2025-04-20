from pydantic import BaseModel
from typing import Literal # Import Literal
class LlamaModel(BaseModel):
    prompt: str
    meal_type: Literal["breakfast", "lunch", "dinner", "snacks"]