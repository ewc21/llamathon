from fastapi import APIRouter, Request
from api.chat_handler import handle_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    return await handle_chat(data["message"])
