from pydantic import BaseModel

class LlamaModel(BaseModel):
    prompt: str