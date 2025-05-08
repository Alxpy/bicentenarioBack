import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.agenda_personal_repository_abstract import IAgendaPersonalRepository
from src.core.models.agenda_personal_domain import AgendaPersonalDomain
from src.presentation.dto.agenda_personal_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.agenda_personal_queries import *

logger = logging.getLogger(__name__)

class AgendaPersonalRepository(IAgendaPersonalRepository):
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
    

    async def get_agenda_personal_by_user(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_AGENDA_PERSONAL_BY_USER, (id,))
            if not result:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=AgendaPersonalDTO(**result),
                message=AGENDA_PERSONAL_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting agenda personal by user: {str(e)}")
            return error_response(
                message=AGENDA_PERSONAL_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def get_all_agendas_personales(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_AGENDA_PERSONAL)
            if not result:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[AgendaPersonalDTO(**row) for row in result],
                message=AGENDA_PERSONAL_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting all agendas personales: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
    async def agenda_personal_by_fecha_user(self, fecha: str, id: int) -> Response:
        try:
            result = await self._execute_query(GET_AGENDA_PERSONAL_BY_FECHA_USER, (fecha, id))
            if not result:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=AgendaPersonalDTO(**result),
                message=AGENDA_PERSONAL_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting agenda personal by fecha and user: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_agenda_personal(self, agenda_personal: AgendaPersonalDTO) -> Response:
        try:
            params = (
                agenda_personal.id_usuario,
                agenda_personal.id_evento,
                agenda_personal.recordatorio,
                agenda_personal.notas
            )
            rowcount = await self._execute_update(CREATE_AGENDA_PERSONAL, params)
            if rowcount == 0:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=AGENDA_PERSONAL_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=AGENDA_PERSONAL_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating agenda personal: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_agenda_personal(self, id: int, agenda_personal: AgendaPersonalUpdateDTO) -> Response:
        try:
            params = (
                agenda_personal.recordatorio,
                agenda_personal.notas,
                id
            )
            rowcount = await self._execute_update(UPDATE_AGENDA_PERSONAL, params)
            if rowcount == 0:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=AGENDA_PERSONAL_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error updating agenda personal: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_agenda_personal(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_AGENDA_PERSONAL, (id,))
            if rowcount == 0:
                return error_response(
                    message=AGENDA_PERSONAL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=AGENDA_PERSONAL_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error deleting agenda personal: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        