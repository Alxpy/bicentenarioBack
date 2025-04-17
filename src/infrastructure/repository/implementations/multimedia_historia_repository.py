import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.multimedia_historia_respository_abstract import IMultimediaHistoriaRepository
from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain
from src.presentation.dto.multimedia_historia_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_historia_queries import *

logger = logging.getLogger(__name__)

class MultimediaHistoriaRepository(IMultimediaHistoriaRepository):
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
    
    async def get_all_multimedia_historia(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_MULTIMEDIA_HISTORIA)
            if not result:
                return error_response(
                    message=MULTIMEDIA_HISTORIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[MultimediaDatosHistoriaDTO(**row) for row in result],
                message=MULTIMEDIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_multimedia_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_multimedia_historia_by_id_historia(self, id_historia: int) -> Response:
        try:
            result = await self._execute_query_all(GET_MULTIMEDIA_HISTORIA_BY_ID_HISTORIA, (id_historia,))
            if not result:
                return error_response(
                    message=MULTIMEDIA_HISTORIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[MultimediaDatosHistoriaDTO(**row) for row in result],
                message=MULTIMEDIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_multimedia_historia_by_id_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_multimedia_historia(self, multimedia_historia: MultimediaHistoriaDTO) -> Response:
        try:
            params=(
                multimedia_historia.id_multimedia,
                multimedia_historia.id_historia
            )
            rowcount = await self._execute_update(CREATE_MULTIMEDIA_HISTORIA, params)
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_HISTORIA_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=MULTIMEDIA_HISTORIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=MULTIMEDIA_HISTORIA_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_multimedia_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_multimedia_historia(self, id_historia: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_MULTIMEDIA_HISTORIA, (id_historia,))
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_HISTORIA_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=MULTIMEDIA_HISTORIA_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in delete_multimedia_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
