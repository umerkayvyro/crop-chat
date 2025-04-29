from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from fastapi import Form
import json
import uuid
from app.services.chat_service import chat_stream

router = APIRouter()

@router.post("/chat")
async def chat(
    conversation_id: str = Form(None),
    prompt: str = Form(...),
):
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    return StreamingResponse(chat_stream(prompt, conversation_id), media_type="application/json")

@router.get("/new_chat")
def new_chat():
    new_uuid = str(uuid.uuid4())
    return {"conversation_id": new_uuid}
