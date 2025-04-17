import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional


from src.core.abstractions.infrastructure.repository.multimedia_cultura_repository_abstract import IMultimediaCulturaRepository
from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain
from src.presentation.dto.multimedia_cultura_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_cultura_queries import *

logger = logging.getLogger(__name__)

class MultimediaCulturaRepository(IMultimediaCulturaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
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
    
    async def get_all_multimedia_cultura(self) -> Response:
        try:
            result = await self._execute_query(GET_ALL_MULTIMEDIA_CULTURA, fetch_all=True)
            if not result:
                return error_response(
                    message=MULTIMEDIA_CULTURA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[MultimediaDatosCulturaDTO(**row) for row in result],
                message=MULTIMEDIA_CULTURA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_multimedia_cultura: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_multimedia_cultura_by_id_cultura(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_MULTIMEDIA_CULTURA_BY_ID_CULTURA, (id,), fetch_all=True)  # <-- Asegura fetch_all=True
            if not result:
                return error_response(
                    message=MULTIMEDIA_CULTURA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[MultimediaDatosCulturaDTO(**row) for row in result],
                message=MULTIMEDIA_CULTURA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_multimedia_cultura_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
        )

    
    async def create_multimedia_cultura(self, multimedia_cultura_dto: MultimediaCulturaDTO) -> Response:
        try:
            params=(
                multimedia_cultura_dto.id_multimedia,
                multimedia_cultura_dto.id_cultura
            )
            rowcount = await self._execute_update(CREATE_MULTIMEDIA_CULTURA, params)
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_CULTURA_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=MULTIMEDIA_CULTURA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=MULTIMEDIA_CULTURA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_multimedia_cultura: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_multimedia_cultura(self, id_cultura: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_MULTIMEDIA_CULTURA, (id_cultura,))
            if rowcount == 0:
                return error_response(
                    message=MULTIMEDIA_CULTURA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=MULTIMEDIA_CULTURA_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in delete_multimedia_cultura: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
            