import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional


from src.core.abstractions.infrastructure.repository.multimedia_repository_abstract import IMultimediaRepository
from src.core.models.multimedia_domain import MultimediaDomain
from src.presentation.dto.multimedia_dto import MultimediaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_queries import *

logger = logging.getLogger(__name__)

class MultimediaRepository(IMultimediaRepository):

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
        
    async def get_all_multimedia(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_MULTIMEDIA)
            if not result:
                return error_response(
                    message=MULTIMEDIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[MultimediaDomain(**row) for row in result],
                message=MULTIMEDIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_multimedia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_multimedia_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_MULTIMEDIA_BY_ID, (id,))
            if not result:
                return error_response(
                    message=MULTIMEDIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=MultimediaDomain(**result),
                message=MULTIMEDIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_multimedia_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_multimedia(self, multimedia_dto: MultimediaDTO) -> Response:
        try:
            params=(
                multimedia_dto.enlace,
                multimedia_dto.tipo
            )
            await self._execute_update(CREATE_MULTIMEDIA, params)
            return success_response(
                message=MULTIMEDIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=MULTIMEDIA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_multimedia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_multimedia(self, id: int, multimedia_dto: MultimediaDTO) -> Response:
        try:
            params=(
                multimedia_dto.enlace,
                multimedia_dto.tipo,
                id
            )
            rowcount = await self._execute_update(UPDATE_MULTIMEDIA, params)
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=MULTIMEDIA_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in update_multimedia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_multimedia(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_MULTIMEDIA, (id,))
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=MULTIMEDIA_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in delete_multimedia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
