from llama_stack_client import LlamaStackClient
from llama_stack_client import Agent, AgentEventLogger
from rich.pretty import pprint
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from auth.security import create_access_token, hash_password, verify_password
from schema.user import UserCreate, UserLogin

from database.dependency import get_db
from schema.llama import LlamaModel

llama_router = APIRouter()

@llama_router.post("/chat")
# TODO: Add authenitcation
def chat(form_data: LlamaModel, db: Session = Depends(get_db)):
    client = LlamaStackClient(base_url=f"http://localhost:11434")

    models = client.models.list()
        
    # llm = next(m for m in models if m.type == "llm")
    llm = models[0]
    model_id = llm.id
    
    print(llm.dict())

    agent = Agent(client, model=model_id, instructions="You are a helpful assistant.")

    s_id = agent.create_session(session_name=f"s{uuid.uuid4().hex}")

    response = agent.create_turn(
        messages=[{"role": "user", "content": form_data.prompt}],
        session_id=s_id,
        stream=False,
    )
    print("agent>", response.output_message.content)
    
    return {"response": response.output_message.content}