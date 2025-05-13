import logging
import os
import re
import asyncio
from datetime import datetime
from typing import Dict, List, Optional


from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

from src.infrastructure.repository.dependency_injection.dependency_injection import get_db_connection
from src.infrastructure.repository.implementations.biblioteca_repository import BibliotecaRepository, BibliotecaDomain
from src.infrastructure.repository.implementations.cultura_repository import CulturaRepository, CulturaDomain
from src.infrastructure.repository.implementations.evento_repository import EventoRepository, EventoDomain
from src.infrastructure.repository.implementations.noticia_repository import NoticiaRepository, NoticiaDomain
from src.infrastructure.repository.implementations.presidente_repository import PresidenteRepository, PresidenteDomain

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Conversation:
    """
    Mantiene el contexto de la conversación.
    """
    def __init__(self):
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente especializado en Bolivia. "
                    "Solo responde sobre temas bolivianos."
                ),
            }
        ]
        self.active: bool = True


_conversations: Dict[str, Conversation] = {}


class ChatService:
    """
    Servicio principal de chat con lógica de consulta y filtrado de datos.
    """
    def __init__(self):
        self.client = Groq(api_key='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')
        self.web_url = os.getenv("WEB_URL", "http://127.0.0.1:5173")

    def get_or_create_conversation(self, conversation_id: str) -> Conversation:
        convo = _conversations.get(conversation_id)
        if convo is None:
            convo = Conversation()
            _conversations[conversation_id] = convo
        return convo

    def _detect_intent(self, query: str) -> Optional[str]:
        intent_keywords = {
            'evento': ['evento', 'fecha', 'festival', 'celebración'],
            'biblioteca': ['libro', 'autor', 'publicación'],
            'presidente': ['presidente', 'gobierno', 'mandato'],
            'cultura': ['cultura', 'tradición', 'patrimonio', 'etnia'],
            'noticia': ['noticia', 'actualidad', 'artículo'],
        }
        q = query.lower()
        for intent, keywords in intent_keywords.items():
            if any(kw in q for kw in keywords):
                return intent
        return None

    def _extract_dates(self, query: str) -> List[datetime]:
        pattern = r'(\d{2}/\d{2}/\d{4})'
        dates = []
        for match in re.findall(pattern, query):
            try:
                dates.append(datetime.strptime(match, '%d/%m/%Y'))
            except ValueError:
                logger.warning(f"Fecha inválida: {match}")
        return dates

    def _apply_evento_filters(self, query: str, eventos: List[EventoDomain]) -> List[EventoDomain]:
        dates = self._extract_dates(query)
        if not dates:
            return eventos
        return [e for e in eventos if any(d.date() == e.fecha_inicio.date() for d in dates)]

    def _apply_presidente_filters(self, query: str, presidentes: List[PresidenteDomain]) -> List[PresidenteDomain]:
        q = query.lower()
        if 'actual' in q or 'current' in q:
            latest = max(presidentes, key=lambda x: x.inicio_periodo)
            return [latest]
        return presidentes

    async def _query_database(self, query: str) -> str:
        intent = self._detect_intent(query)
        if not intent:
            return "No puedo determinar el tema de tu consulta"
        logger.info(f"Intent detected: {intent}")

        mapper = {
            'evento': self.intention_evento,
            'biblioteca': self.intention_biblioteca,
            'presidente': self.intention_presidente,
            'cultura': self.intention_cultura,
            'noticia': self.intention_noticia,
        }
        # Ejecutar método de intención y await si es coroutine
        handler = mapper[intent]
        data = handler()
        if asyncio.iscoroutine(data):
            data = await data
        data = data or []
        if not data:
            return f"No se encontraron datos de {intent}"
        logger.info(f"Data retrieved for intent {intent}: {data}")

        if intent == 'evento':
            data = self._apply_evento_filters(query, data)
        elif intent == 'presidente':
            data = self._apply_presidente_filters(query, data)

        parts = []
        for item in data:
            link = f"{self.web_url}/{intent}/{item.id}"
            if intent == 'evento':
                parts.append(
                    f"Evento: {item.nombre}\n"
                    f"Fecha: {item.fecha_inicio.strftime('%d/%m/%Y')} - {item.fecha_fin.strftime('%d/%m/%Y')}\n"
                    f"Enlace: {link}\n"
                )
            elif intent == 'presidente':
                parts.append(
                    f"Presidente: {item.nombre} {item.apellido}\n"
                    f"Periodo: {item.inicio_periodo} - {item.fin_periodo}\n"
                    f"Enlace: {link}\n"
                )
        return "\n".join(parts) if parts else "No se encontraron resultados"

    async def query_groq_api(self, conversation: Conversation) -> str:
        try:
            user_msgs = [m for m in conversation.messages if m['role'] == 'user']
            if not user_msgs:
                return "Por favor haz una pregunta sobre Bolivia"

            last = user_msgs[-1]['content']
            if self._detect_intent(last):
                return await self._query_database(last)

            completion = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=conversation.messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1.0,
                stream=True,
            )

            # Corregir iteración asíncrona
            response_content = []
            async for chunk in completion:
                if chunk.choices[0].delta.content:
                    response_content.append(chunk.choices[0].delta.content)
            
            return "".join(response_content)

        except Exception:
            logger.exception("Error en procesamiento")
            return "Ocurrió un error al procesar tu solicitud"

    async def intention_biblioteca(self) -> List[BibliotecaDomain]:
        repo = BibliotecaRepository(get_db_connection())
        return await repo.get_all_bibliotecas()

    async def intention_presidente(self) -> List[PresidenteDomain]:
        repo = PresidenteRepository(get_db_connection())
        return await repo.get_all_presidentes()

    async def intention_cultura(self) -> List[CulturaDomain]:
        repo = CulturaRepository(get_db_connection())
        return await repo.get_all_cultura()

    async def intention_noticia(self) -> List[NoticiaDomain]:
        repo = NoticiaRepository(get_db_connection())
        return await repo.get_all_noticias()


# Fábrica de servicio
def get_chat_service() -> ChatService:
    api_key = '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'
    return ChatService()
