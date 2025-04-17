import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.categoria_historia_repository_abstract import ICategoriaHistoriaRepository
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.categoria_historia_queries import *

logger = logging.getLogger(__name__)

class CategoriaHistoriaRepository(ICategoriaHistoriaRepository):
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
    

    async def get_all_categorias_historia(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_CATEGORIA_HISTORIA)
            if not result:
                return error_response(
                    message=CATEGORIA_HISTORIA_NOT_FOUND_MSG,

                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[CategoriaHistoriaDomain(**row) for row in result],
                message=CATEGORIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_categoria_historia(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_CATEGORIA_HISTORIA_BY_ID, (id,))
            if not result:
                return error_response(
                    message=CATEGORIA_HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=CategoriaHistoriaDomain(**result),
                message=CATEGORIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_categoria_historia_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_categoria_historia(self, categoria_historia: CategoriaHistoriaDTO) -> Response:
        try:
            params=(
                categoria_historia.nombre,
                categoria_historia.descripcion
            )
            await self._execute_update(CREATE_CATEGORIA_HISTORIA, params)
            return success_response(
                message=CATEGORIA_HISTORIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in create_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    async def update_categoria_historia(self, id: int, categoria_historia: CategoriaHistoriaDomain) -> Response:
        try:
            params=(
                categoria_historia.nombre,
                categoria_historia.descripcion,
                id
            )
            await self._execute_update(UPDATE_CATEGORIA_HISTORIA, params)
            return success_response(
                message=CATEGORIA_HISTORIA_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in update_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in update_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_categoria_historia(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_CATEGORIA_HISTORIA, (id,))
            if rowcount == 0:
                return error_response(
                    message=CATEGORIA_HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=CATEGORIA_HISTORIA_DELETED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in delete_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in delete_categoria_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
            


        

