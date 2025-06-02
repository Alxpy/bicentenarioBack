import os
import logging
from typing import Dict, List

from pydantic import BaseModel, Field
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": "Eres un asistente de IA que ayuda a los usuarios a encontrar información."},
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

    def _is_db_topic(self, query: str) -> bool:
            """Determina si la consulta requiere información de la base de datos"""
            keywords = [
                 'gobierno'
            ]
        #    'libro', 'historia', 'etnia', 
        #        'noticia', 'presidente', 'evento',
        #        'literatura', 'cultura',
            return any(keyword in query.lower() for keyword in keywords)
        
    def _query_database(self, query: str) -> str:
       
        db_data = {
            'libros': "Libro destacado: 'Juan de la Rosa' de Nataniel Aguirre",
            'presidentes': "Presidente actual: Luis Arce Catacora (desde 2020)",
            'etnias': "Principales grupos étnicos: Quechua, Aymara, Guaraní"
        }
        
        for key in db_data:
            if key in query.lower():
                return f"[Base de datos] {db_data[key]}"
        
        return "[Base de datos] Información no encontrada"

    def query_groq_api(self, conversation: Conversation) -> str:
        try:
                        
            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=conversation.messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                stream=True,
            )
            return ''.join(chunk.choices[0].delta.content or '' for chunk in completion)
            
        except Exception:
            logger.exception("Error en procesamiento")
            return "Ocurrió un error al procesar tu solicitud"


def get_chat_service() -> ChatService:
    api_key = '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'
    return ChatService(api_key=api_key)