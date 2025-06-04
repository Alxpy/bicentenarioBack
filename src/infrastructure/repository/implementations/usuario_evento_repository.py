import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.usuario_evento_repository_abstract import IUsuarioEventoRepository
from src.core.models.usuario_evento_domain import UsuarioEventoDomain
from src.presentation.dto.usuario_evento_dto import UsuarioEventoDTO, UpdateAsistioUsuarioEventoDTO, UsuarioEventoData
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.usuario_evento_queries import *


logger = logging.getLogger(__name__)

class UsuarioEventoRepository(IUsuarioEventoRepository):
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
        
    
    async def get_usuario_evento_by_id_usuario(self, id: int) -> Response:
        try:
            result = await self._execute_query_all(GET_USUARIO_EVENTO_BY_ID_USUARIO, (id,))
            if not result:
                return error_response(
                    message=USUARIO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=USUARIO_EVENTO_FOUND_MSG,
                data=[UsuarioEventoDomain(**row) for row in result],
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting user event by user ID: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_usuario_evento_by_id_evento(self, id: int) -> Response:
        try:
            result = await self._execute_query_all(GET_USUARIO_EVENTOS_BY_ID_EVENTO, (id,))
            if not result:
                return error_response(
                    message=USUARIO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=USUARIO_EVENTO_FOUND_MSG,
                data=[UsuarioEventoDomain(**row) for row in result],
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting user events by event ID: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_all_usuario_eventos(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_USUARIO_EVENTOS)
            if not result:
                return error_response(
                    message=USUARIO_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[UsuarioEventoDomain(**row) for row in result],
                message=USUARIO_EVENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting all user events: {str(e)}")
            return error_response(
                message=USUARIO_EVENTO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )

    async def create_usuario_evento(self, usuario_evento: UsuarioEventoDTO) -> Response:
        try:
            params = (usuario_evento.id_usuario, usuario_evento.id_evento, usuario_evento.asistio)
            rowcount = await self._execute_update(CREATE_USUARIO_EVENTO, params)
            if rowcount == 0:
                return error_response(
                    message=USUARIO_EVENTO_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=USUARIO_EVENTO_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=f"{USUARIO_EVENTO_NOT_CREATED_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating user event: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_asistio_usuario_evento(self, id: int, asistio: UpdateAsistioUsuarioEventoDTO) -> Response:
        try:
            params = (asistio.asistio, id)
            rowcount = await self._execute_update(UPDATE_ASISTIO_USUARIO_EVENTO, params)
            if rowcount == 0:
                return error_response(
                    message=USUARIO_EVENTO_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=USUARIO_EVENTO_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error updating user event: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_usuario_evento(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_USUARIO_EVENTO, (id,))
            if rowcount == 0:
                return error_response(
                    message=USUARIO_EVENTO_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=USUARIO_EVENTO_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error deleting user event: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    

    async def get_data_usuario_evento(self) -> Response:
        try:
            result = await self._execute_query_all(GET_DATA_USUARIO_EVENTO)
            if not result:
                return error_response(
                    message=USUARIO_ROL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[UsuarioEventoData(**row) for row in result],
                message=USUARIO_ROL_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting user role data: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )