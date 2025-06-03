from src.core.abstractions.services.notificacion_service_abstract import INotificacionService
from src.core.abstractions.infrastructure.repository.notificacion_repository_abstract import INotificacionRepositoryAbstract
from src.core.models.notificacion_domain import NotificacionDomain
from src.presentation.dto.notificacion_dto import NotificacionDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.patrosinador_queries import *
from typing import Optional, List

import logging

logger = logging.getLogger(__name__)


class NotificacionRepository(INotificacionRepositoryAbstract):
    def __init__(self, connection):
        self.connection = connection

    async def _execute_query(self, query: str, params: tuple = None) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
    
    async def _execute_query_all(self, query: str, params: tuple = None) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
        
    
