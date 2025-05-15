import os
import logging

from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks, APIRouter
from dotenv import load_dotenv
from src.core.services.chat_service import ChatService, get_chat_service, _conversations
from src.presentation.dto.chat_dto import UserInput
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

@chat_router.post("/", summary="Send a message and receive assistant response")
async def chat(
    user_input: UserInput,
    chat_service: ChatService = Depends(get_chat_service)
):
    convo = chat_service.get_or_create_conversation(user_input.conversation_id)
    if not convo.active:
        raise HTTPException(status_code=400, detail="Conversation is inactive.")

    convo.messages.append({"role": user_input.role, "content": user_input.message})

    try:
        assistant_text = chat_service.query_groq_api(convo)
        convo.messages.append({"role": "assistant", "content": assistant_text})
    except Exception as exc:
        logger.error(f"Failed to query assistant: {exc}")
        raise HTTPException(status_code=500, detail="Error fetching assistant response.")

    return {"response": assistant_text, "conversation_id": user_input.conversation_id}

@chat_router.get("/{conversation_id}", summary="Get full conversation history")
async def get_conversation(conversation_id: str):
    convo = _conversations.get(conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return {"conversation_id": conversation_id, "messages": convo.messages}