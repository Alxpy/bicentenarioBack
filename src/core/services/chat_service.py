import os
import logging
from typing import Dict

from pydantic import BaseModel, Field
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Conversation:
    def __init__(self):
        self.messages: list[Dict[str, str]] = [
            {"role": "system", "content": "You are a helpful assistant and you only answer about Bolivia."}
        ]
        self.active: bool = True

_conversations: Dict[str, Conversation] = {}

class ChatService:
    def __init__(self, api_key: str):
        if not api_key:
            logger.error("GROQ_API_KEY is missing")
            raise ValueError("GROQ_API_KEY must be provided")
        self.client = Groq(api_key=api_key)

    def get_or_create_conversation(self, conversation_id: str) -> Conversation:
        convo = _conversations.get(conversation_id)
        if convo is None:
            convo = Conversation()
            _conversations[conversation_id] = convo
        return convo

    def query_groq_api(self, conversation: Conversation) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=conversation.messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                stream=True,
            )
            return ''.join(chunk.choices[0].delta.content or '' for chunk in completion)
        except Exception:
            logger.exception("Error querying GROQ API")
            raise


def get_chat_service() -> ChatService:
    api_key = os.getenv("GROQ_API_KEY")
    return ChatService(api_key=api_key)