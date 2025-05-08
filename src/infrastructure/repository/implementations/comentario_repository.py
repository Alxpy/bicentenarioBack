import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.comentario_repository_abstract import IComentarioRepository
from src.core.models.comentario_domain import ComentarioDomain
from src.presentation.dto.comentario_dto import ComentarioDTO, ComentarioUpdateDTO,ComentarioResponseCreate
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.comentario_queries import *

logger = logging.getLogger(__name__)

class ComentarioRepository(IComentarioRepository):
    
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
    
    
    async def get_all_comentarios(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_COMENTARIOS)
            if not result:
                return error_response(
                    message=COMENTARIO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[ComentarioDomain(**row) for row in result],
                message=COMENTARIO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting all comentarios: {str(e)}")
            return error_response(
                message=COMENTARIO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def get_comentario_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_COMENTARIO_BY_ID, (id,))
            if not result:
                return error_response(
                    message=COMENTARIO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=ComentarioDomain(**result),
                message=COMENTARIO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting comentario by id: {str(e)}")
            return error_response(
                message=COMENTARIO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def create_comentario(self, comentario_dto: ComentarioDTO) -> Response:
        try:
            params = (
                comentario_dto.id_usuario,
                comentario_dto.contenido,
                comentario_dto.fecha_creacion
            )
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_COMENTARIO, params)
                self.connection.commit()
                id_comentario = cursor.lastrowid
                logger.info(f"Comentario created with ID: {id_comentario}")
                return success_response(
                    message=COMENTARIO_CREATED_MSG,
                    status=HTTP_201_CREATED,
                    data=ComentarioResponseCreate(
                        id=id_comentario,
                    )
                )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=COMENTARIO_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating comentario: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_comentario(self, id: int, comentario_dto: ComentarioUpdateDTO) -> Response:
        try:
            params = (
                comentario_dto.contenido,
                comentario_dto.fecha_creacion,
                id
            )
            rowcount = await self._execute_update(UPDATE_COMENTARIO, params)
            if rowcount == 0:
                return error_response(
                    message=COMENTARIO_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error updating comentario: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_comentario(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_COMENTARIO, (id,))
            if rowcount == 0:
                return error_response(
                    message=COMENTARIO_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_DELETED_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error deleting comentario: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    
