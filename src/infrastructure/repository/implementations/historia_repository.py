import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.historia_repository_abstract import IHistoriaRepository
from src.core.models.historia_domain import HistoriaDomain
from src.presentation.dto.historia_dto import *
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.historia_queries import *

logger = logging.getLogger(__name__)

class HistoriaRepository(IHistoriaRepository):
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
    
    
    async def get_all_historia(self) -> Response:
        try:
            result = await self._execute_query(GET_ALL_HISTORIA, fetch_all=True)
            if not result:
                return error_response(
                    message=HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[HistoriaDomain(**row) for row in result],
                message=HISTORIAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_historias: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_historia_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_HISTORIA_BY_ID, (id,))
            if not result:
                return error_response(
                    message=HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=HistoriaDomain(**result),
                message=HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_historia_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_historia_by_titulo(self, titulo: str) -> Response:
        try:
            result = await self._execute_query(GET_HISTORIA_BY_TITULO, (titulo,))
            if not result:
                return error_response(
                    message=HISTORIA_BY_TITULO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=HistoriaDomain(**result),
                message=HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_historia_by_titulo: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_historia_by_ubicacion(self, ubicacion: str) -> Response:
        try:
            result = await self._execute_query(GET_HISTORIA_BY_UBICACION, (ubicacion,))
            if not result:
                return error_response(
                    message=HISTORIA_BY_UBICACION_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[HistoriaDomain(**row) for row in result],
                message=HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_historia_by_ubicacion: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_historia_by_categoria(self, categoria: str) -> Response:
        try:
            result = await self._execute_query(GET_HISTORIA_BY_CATEGORIA, (categoria,))
            if not result:
                return error_response(
                    message=HISTORIA_BY_CATEGORIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[HistoriaDomain(**row) for row in result],
                message=HISTORIAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_historia_by_categoria: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_historia(self, historia: HistoriaDTO) -> Response:
        try:
            params=(
                historia.titulo,
                historia.descripcion,
                historia.fecha_inicio,
                historia.fecha_fin,
                historia.imagen,
                historia.id_ubicacion,
                historia.id_categoria
            )
            await self._execute_update(CREATE_HISTORIA, params)
            return success_response(
                message=HISTORIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"IntegrityError in create_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in create_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def update_historia(self, id: int, historia: HistoriaDomain) -> Response:
        try:
            params=(
                historia.titulo,
                historia.descripcion,
                historia.fecha_inicio,
                historia.fecha_fin,
                historia.imagen,
                historia.id_ubicacion,
                historia.id_categoria,
                id
            )
            rowcount = await self._execute_update(UPDATE_HISTORIA, params)
            if rowcount == 0:
                return error_response(
                    message=HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=HISTORIA_UPDATED_MSG
            )
        except IntegrityError as e:
            logger.error(f"IntegrityError in update_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in update_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_historia(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_HISTORIA, (id,))
            if rowcount == 0:
                return error_response(
                    message=HISTORIA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=HISTORIA_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error in delete_historia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
