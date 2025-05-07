import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.tipo_evento_repository_abstract import ITipoEventoRepository
from src.core.models.tipo_evento_domain import TipoEventoDomain
from src.presentation.dto.tipo_evento_dto import TipoEventoDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.tipo_evento_queries import *


logger = logging.getLogger(__name__)

class TipoEventoRepository(ITipoEventoRepository):
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
        
    
    async def get_all_tipo_eventos(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_TIPO_EVENTO)
            if not result:
                return error_response(
                    message=TIPO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[TipoEventoDTO(**row) for row in result],
                message=TIPO_EVENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting all tipo_eventos: {str(e)}")
            return error_response(
                message=TIPO_EVENTO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def get_tipo_evento_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_TIPO_EVENTO_BY_ID, (id,))
            if not result:
                return error_response(
                    message=TIPO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=TipoEventoDTO(**result),
                message=TIPO_EVENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting tipo_evento by id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_tipo_evento(self, tipo_evento: TipoEventoDTO) -> Response:
        try:
            params = (tipo_evento.nombre_evento,)
            rowcount = await self._execute_update(CREATE_TIPO_EVENTO, params)
            if rowcount == 0:
                return error_response(
                    message=TIPO_EVENTO_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=TIPO_EVENTO_CREATED_MSG,
                status=HTTP_201_CREATED,
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=f"{TIPO_EVENTO_NOT_CREATED_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating tipo_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_tipo_evento(self, id: int, tipo_evento: TipoEventoDomain) -> Response:
        try:
            params = (tipo_evento.nombre_evento, id)
            rowcount = await self._execute_update(UPDATE_TIPO_EVENTO, params)
            if rowcount == 0:
                return error_response(
                    message=TIPO_EVENTO_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=TIPO_EVENTO_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error updating tipo_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_tipo_evento(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_TIPO_EVENTO, (id,))
            if rowcount == 0:
                return error_response(
                    message=TIPO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=TIPO_EVENTO_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error deleting tipo_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    