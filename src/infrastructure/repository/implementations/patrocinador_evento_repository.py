from src.core.models.patrocinador_evento_domain import PatrocinadorEvento
from src.presentation.responses.base_response import Response
from src.infrastructure.queries.patrocinador_evento_queries import *
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.presentation.responses.response_factory import success_response, error_response
from src.presentation.dto.patrocinador_evento_dto import PatrocinadorEventoByEvento
import logging
logger = logging.getLogger(__name__)
from  typing import Optional, List


class PatrocinadorEventoRepository:
    
    def __init__(self, connection):
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
    
    async def create_patrocinador_evento(self, patrocinador_evento: PatrocinadorEvento) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_PATROCINADOR_EVENTO, (patrocinador_evento.id_evento, patrocinador_evento.id_patrocinador))
                self.connection.commit()
                return success_response(
                    message=PATROCINADOR_EVENTO_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
        except Exception as e:
            logger.error(f"Error creating patrocinador_evento: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_patrocinador_by_evento(self, id_evento: int) -> Response:
        try:
            result = await self._execute_query_all(GET_PATROCINADOR_EVENTO_BY_EVENTO, (id_evento,))
            if not result:
                return error_response(
                    message=PATROCINADOR_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            logger.info(f"Patrocinador by evento: {result}")
            return success_response(
                message=PATROCINADOR_EVENTO_FOUND_MSG,
                data=[PatrocinadorEventoByEvento(**row) for row in result],
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting patrocinador by evento: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_evento_by_patrocinador(self, id_patrocinador: int) -> Response:
        try:
            result = self._execute_query_all(GET_PATROCINADOR_EVENTO_BY_PATROCINADOR, (id_patrocinador,))
            if not result:
                return error_response(
                    message=PATROCINADOR_EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=PATROCINADOR_EVENTO_FOUND_MSG,
                data=result,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by patrocinador: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    