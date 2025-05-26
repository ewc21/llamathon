from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserCreate(BaseModel):
    username: str
    password: str
    height: float
    multiplier: str
    name: str
    age: int
class LlamaModel(BaseModel):
    prompt: str