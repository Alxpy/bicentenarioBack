import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.comentario_evento_repository_abstract import IComentarioEventoRepository
from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_evento_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.comentario_evento_queries import *

logger = logging.getLogger(__name__)

class ComentarioEventoRepository(IComentarioEventoRepository):
    def __init__(self, connection) -> None:
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
    
    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización y retorna el rowcount"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")
    
    async def get_all_comentario_evento(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_COMENTARIO_EVENTO)
            if not result:
                return error_response(
                    status=404,
                    success=False,
                    message=COMENTARIO_EVENTO_NOT_FOUND_MSG,
                    data=None
                )
            
            processed_result = []
            for row in result:
                if 'fecha_creacion' in row and isinstance(row['fecha_creacion'], date):
                    row['fecha_creacion'] = row['fecha_creacion'].isoformat()
                processed_result.append(row)
            
            return success_response(
                message=COMENTARIO_EVENTO_FOUND_MSG,
                data=[ComentarioDatosEventoDTO(**row) for row in processed_result]
            )
            
        except Exception as e:
            logger.error(f"Error getting all comentario_evento: {str(e)}")
            return error_response(
                status=404,
                success=False,
                message=COMENTARIO_EVENTO_NOT_FOUND_MSG,
                data=None
            )
    
    async def get_comentario_evento_by_id_evento(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_COMENTARIO_EVENTO_BY_ID_EVENTO, (id,))
            if not result:
                return error_response(
                    message=COMENTARIO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[ComentarioEventoDTO(**row) for row in result],
                message=COMENTARIO_EVENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting comentario_evento by id_evento: {str(e)}")
            return error_response(
                message=COMENTARIO_EVENTO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def create_comentario_evento(self, comentario_evento: ComentarioEventoDTO) -> None:
        try:
            result = await self._execute_update(CREATE_COMENTARIO_EVENTO, (comentario_evento.id_evento, comentario_evento.id_comentario))
            if result == 0:
                return error_response(
                    message=COMENTARIO_EVENTO_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_EVENTO_CREATED_MSG
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=COMENTARIO_EVENTO_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating comentario_evento: {str(e)}")
            return error_response(
                message=COMENTARIO_EVENTO_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
    
    async def delete_comentario_evento(self, id: int) -> None:
        try:
            result = await self._execute_update(DELETE_COMENTARIO_EVENTO, (id,))
            if result == 0:
                return error_response(
                    message=COMENTARIO_EVENTO_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_EVENTO_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error deleting comentario_evento: {str(e)}")
            return error_response(
                message=COMENTARIO_EVENTO_NOT_DELETED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
    


