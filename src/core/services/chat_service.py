import os
import logging
from typing import Dict, List

import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Conversation:
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": (
                "Eres un asistente especializado en Bolivia. "
                "Solo responde sobre temas bolivianos."
            )}
        ]
        self.active: bool = True


_conversations: Dict[str, Conversation] = {}


class ChatService:
    def __init__(self, api_key: str):
        if not api_key:
            logger.error("GROQ_API_KEY is missing")
            raise ValueError("GROQ_API_KEY must be provided")
        self.client = Groq(api_key=api_key)
        self.server_url = os.getenv("SERVER_URL")  # e.g. http://127.0.0.1:8000
        self.web_url = os.getenv("WEB_URL")        # e.g. http://127.0.0.1:5173

    def get_or_create_conversation(self, conversation_id: str) -> Conversation:
        convo = _conversations.get(conversation_id)
        if convo is None:
            convo = Conversation()
            _conversations[conversation_id] = convo
        return convo

    def _is_db_topic(self, query: str) -> bool:
        keywords = [
            'libro', 'historia', 'etnia', 'noticia',
            'presidente', 'evento', 'literatura', 'cultura', 'gobierno'
        ]
        return any(keyword in query.lower() for keyword in keywords)

    def _handle_db_intent(self, query: str) -> str:
        """
        Llama al endpoint REST correspondiente según la intención del usuario,
        formatea la respuesta manteniendo el esquema {status, success, message, data}
        y agrega enlaces web para cada elemento.
        """
        # Mapeo de palabra clave a ruta API y ruta web para enlaces
        mapping = {
            'libro':    {'api': '/api/v1/library',  'web': '/showhistoria'},
            'literatura':{'api': '/api/v1/library', 'web': '/showhistoria'},
            'historia': {'api': '/api/v1/history',  'web': '/showhistoria'},
            'etnia':    {'api': '/api/v1/cultures', 'web': '/cultura/:id'},
            'cultura':  {'api': '/api/v1/cultures', 'web': '/cultura/:id'},
            'noticia':  {'api': '/api/v1/news',     'web': '/cultura/:id'},
            'presidente':{'api': '/api/v1/president','web': '/presidente/detalle'},
            'evento':   {'api': '/api/v1/evento',   'web': '/evento/:id'},
            'gobierno': {'api': '/api/v1/government','web': '/gobierno/:id'},
        }
        # Encontrar la primera intención coincidente
        intent = next((k for k in mapping if k in query.lower()), None)
        if not intent:
            return "[Base de datos] Tema reconocido, pero no implementado."

        routes = mapping[intent]
        url = f"{self.server_url}{routes['api']}"
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            payload = resp.json()

            # Agregar enlace en cada elemento de data
            for item in payload.get('data', []):
                id_val = item.get('id')
                # Reemplazar placeholder :id en web route
                web_path = routes['web'].replace(':id', str(id_val))
                item['enlace'] = f"{self.web_url}{web_path}"

            # Devolver JSON como string (manteniendo llaves y estructura)
            return payload
        except requests.RequestException:
            logger.exception("Error consultando API externa")
            return {
                "status": -1,
                "success": False,
                "message": "Error al conectarse al servicio externo",
                "data": []
            }

    def query_groq_api(self, conversation: Conversation) -> str:
        try:
            user_questions = [m for m in conversation.messages if m['role'] == 'user']
            if not user_questions:
                return "Por favor haz una pregunta sobre Bolivia"

            last_query = user_questions[-1]['content']

            if self._is_db_topic(last_query):
                return self._handle_db_intent(last_query)

            # Para otros temas, consulta al modelo Groq
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
            logger.exception("Error en procesamiento")
            return "Ocurrió un error al procesar tu solicitud"


def get_chat_service() -> ChatService:
    api_key = os.getenv("GROQ_API_KEY")
    return ChatService(api_key=api_key)
