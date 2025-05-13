import logging
from typing import List, Optional
from src.core.models.expositor_domain import ExpositorDomain
from src.presentation.dto.expositor_dto import ExpositorCreate
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.expositor_queries import *

logger = logging.getLogger(__name__)

class ExpositorRepository:
    
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
            
    async def get_all(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_EXP)
            if not result:
                return error_response(
                    message='Expositores no encontrados',
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[ExpositorDomain(**row) for row in result],
                message=MULTIMEDIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_expositores: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    async def create(self, expositor: ExpositorCreate) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_EXP, (expositor.nombre,))
                self.connection.commit()  # CORRECTO: commit en la conexión
                id = cursor.lastrowid
                logger.info(f"Expositor created with ID: {id}")
                return success_response(
                    message='EXPOSITOR_CREATED',
                    status=HTTP_201_CREATED,
                    data=ExpositorDomain(id=id, nombre=expositor.nombre)
                )
        except Exception as e:
            logger.error(f"Error in create_expositor: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    
    async def create_expositor_evento(self, id_evento: int, id_expositor: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_EXP_EVENT, (id_evento, id_expositor))
                self.connection.commit()
                return success_response(
                    message='EXPOSITOR_EVENTO_CREATED',
                    status=HTTP_201_CREATED
                )
        except Exception as e:
            logger.error(f"Error in create_expositor_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    async def get_all_expositores_by_evento(self, id_evento: int) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_EXP_BY_EVENT, (id_evento,))
            if not result:
                return error_response(
                    message='Expositores no encontrados',
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[ExpositorDomain(**row) for row in result],
                message=MULTIMEDIA_HISTORIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_expositores_by_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    async def delete_expositor_evento(self, id_evento: int, id_expositor: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DELETE_EXP_EVENT, (id_evento, id_expositor))
                self.connection.commit()
                return success_response(
                    message='EXPOSITOR_EVENTO_DELETED',
                    status=HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error in delete_expositor_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
            