import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.presidente_repository_abstract import IPresidenteRepository
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.dto.presidente_dto import PresidenteDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.presidente_queries import *

logger = logging.getLogger(__name__)

class PresidenteRepository(IPresidenteRepository):
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
            

    async def get_all_presidentes(self) -> Response:
        try:
            result = await self._execute_query(GET_ALL_PRESIDENTES, fetch_all=True)
            if not result:
                return error_response(
                    message=NO_PRESIDENTE_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[PresidenteDomain(**row) for row in result],
                message=PRESIDENTES_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_presidentes: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_presidente_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_PRESIDENTE_BY_ID, (id,))
            if not result:
                return error_response(
                    message=PRESIDENTE_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=PresidenteDomain(**result),
                message=PRESIDENTE_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_presidente_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_presidente_by_nombre(self, nombre: str) -> Response:
        try:
            result = await self._execute_query(GET_PRESIDENTE_BY_NOMBRE, (nombre,))
            if not result:
                return error_response(
                    message=NO_PRESIDENTE_BY_NOMBRE_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=PresidenteDomain(**result),
                message=PRESIDENTE_BY_NAMBRE_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_presidente_by_nombre: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_presidente(self, presidente_dto: PresidenteDTO) -> Response:
        try:
            params = (
                presidente_dto.nombre,
                presidente_dto.apellido,
                presidente_dto.imagen,
                presidente_dto.inicio_periodo,
                presidente_dto.fin_periodo,
                presidente_dto.bibliografia,
                presidente_dto.partido_politico,
                presidente_dto.principales_politicas,
                presidente_dto.id_usuario
            )
            await self._execute_update(CREATE_PRESIDENTE, params)
            return success_response(
                message=PRESIDENTE_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=PRESIDENTE_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_presidente: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_presidente(self, id: int, presidente_dto: PresidenteDTO) -> Response:
        try:
            params = (
                presidente_dto.nombre,
                presidente_dto.apellido,
                presidente_dto.imagen,
                presidente_dto.inicio_periodo,
                presidente_dto.fin_periodo,
                presidente_dto.bibliografia,
                presidente_dto.partido_politico,
                presidente_dto.principales_politicas,
                presidente_dto.id_usuario,
                id
            )
            rowcount = await self._execute_update(UPDATE_PRESIDENTE, params)
            if rowcount == 0:
                return error_response(
                    message=PRESIDENTE_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=PRESIDENTE_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error in update_presidente: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_presidente(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_PRESIDENTE, (id,))
            if rowcount == 0:
                return error_response(
                    message=PRESIDENTE_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=PRESIDENTE_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error in delete_presidente: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )