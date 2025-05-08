import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.usuario_rol_repository_abstract import IUsuarioRolRepository
from src.core.models.usuario_rol_domain import UsuarioRolDomain
from src.presentation.dto.usuario_rol_dto import UsuarioRolDTO,UsuarioRolDataDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.usuario_rol_queries import *


logger = logging.getLogger(__name__)

class UsuarioRolRepository(IUsuarioRolRepository):
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
    
    async def get_all_usuario_roles(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_USUARIO_ROL)
            if not result:
                return error_response(
                    message=USUARIO_ROL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[UsuarioRolDataDTO(**row) for row in result],
                message=USUARIO_ROL_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting all user roles: {str(e)}")
            return error_response(
                message=INTERNAL_SERVER_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=INTERNAL_SERVER_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_usuario_rol_by_id_rol(self, id: int) -> Response:
        try:
            result = await self._execute_query_all(GET_USUARIO_ROL_BY_ID_ROL, (id,))
            if not result:
                return error_response(
                    message=USUARIO_ROL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[UsuarioRolDataDTO(**row) for row in result],
                message=USUARIO_ROL_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting user role by ID: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
    async def create_usuario_rol(self, usuario_rol: UsuarioRolDTO) -> Response:
        try:
            result = await self._execute_update(CREATE_USUARIO_ROL, (usuario_rol.id_usuario, usuario_rol.id_rol))
            if result == 0:
                return error_response(
                    message=USUARIO_ROL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=USUARIO_ROL_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error creating user role: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_usuario_rol(self, id: int) -> Response:
        try:
            result = await self._execute_update(DELETE_USUARIO_ROL, (id,))
            if result == 0:
                return error_response(
                    message=USUARIO_ROL_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=USUARIO_ROL_DELETED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error deleting user role: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    