import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.comentario_biblioteca_repository_abstract import IComentarioBibliotecaRepository
from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_biblioteca_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.comentario_biblioteca_queries import *


logger = logging.getLogger(__name__)

class ComentarioBibliotecaRepository(IComentarioBibliotecaRepository):
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
    

    async def get_all_comentario_biblioteca(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_COMENTARIO_BIBLIOTECA)
            logger.info(result)
            if not result:
                return error_response(
                    message=COMENTARIO_BIBLIOTECA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            # Convertir las fechas a string ISO
            processed_result = []
            for row in result:
                if 'fecha_creacion' in row and isinstance(row['fecha_creacion'], date):
                    row['fecha_creacion'] = row['fecha_creacion'].isoformat()
                processed_result.append(row)
            
            return success_response(
                data=[ComentarioDatosBibliotecaDTO(**row) for row in processed_result],
                message=COMENTARIO_BIBLIOTECA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting all comentario_biblioteca: {str(e)}")
            return error_response(
                message=COMENTARIO_BIBLIOTECA_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
    
    async def get_comentario_biblioteca_by_id_biblioteca(self, id: int) -> Response:
        try:
            result = await self._execute_query_all(GET_COMENTARIO_BIBLIOTECA_BY_ID_BIBLIOTECA, (id,))
            if not result:
                return error_response(
                    message=COMENTARIO_BIBLIOTECA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            # Convertir las fechas a string ISO
            processed_result = []
            for row in result:
                if 'fecha_creacion' in row and isinstance(row['fecha_creacion'], date):
                    row['fecha_creacion'] = row['fecha_creacion'].isoformat()
                processed_result.append(row)
            return success_response(
                data=[ComentarioDatosBibliotecaDTO(**row) for row in processed_result],
                message=COMENTARIO_BIBLIOTECA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error getting comentario_biblioteca by id: {str(e)}")
            return error_response(
                message=COMENTARIO_BIBLIOTECA_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
        
    async def create_comentario_biblioteca(self, comentario_biblioteca: ComentarioBibliotecaDTO) -> None:
        try:
            logger.info(f"Creating comentario_biblioteca: {comentario_biblioteca}")
            result = await self._execute_update(CREATE_COMENTARIO_BIBLIOTECA, (comentario_biblioteca.id_biblioteca, comentario_biblioteca.id_comentario))
            if result == 0:
                return error_response(
                    message=COMENTARIO_BIBLIOTECA_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_BIBLIOTECA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=COMENTARIO_BIBLIOTECA_NOT_CREATED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating comentario_biblioteca: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_comentario_biblioteca(self, id: int) -> None:
        try:
            result = await self._execute_update(DELETE_COMENTARIO_BIBLIOTECA, (id,))
            if result == 0:
                return error_response(
                    message=COMENTARIO_BIBLIOTECA_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=COMENTARIO_BIBLIOTECA_DELETED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error: {str(e)}")
            return error_response(
                message=COMENTARIO_BIBLIOTECA_NOT_DELETED_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting comentario_biblioteca: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    

