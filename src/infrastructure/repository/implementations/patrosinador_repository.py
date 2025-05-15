from src.core.abstractions.infrastructure.repository.patrosinador_repository_abstrac import IPatrocinadorRepositoryAbstract
from src.presentation.dto.patrocinador_dto import PatrocinadorCreateDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.core.models.patrocinador_domain import PatrocinadorDomain
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.patrosinador_queries import *
import logging
logger = logging.getLogger(__name__)
from  typing import Optional, List

class PatrocinadorRepository(IPatrocinadorRepositoryAbstract):
    
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
            

    
    async def create(self, patrocinador: PatrocinadorCreateDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_PATROCINADOR, (patrocinador.nombre, patrocinador.imagen, patrocinador.contacto))
                self.connection.commit()
                id = cursor.lastrowid
                return success_response(
                    message=PATROCINADOR_CREATED_MSG,
                    status=HTTP_201_CREATED,
                    data=PatrocinadorDomain(
                        id=id,
                        nombre=patrocinador.nombre,
                        imagen=patrocinador.imagen,
                        contacto=patrocinador.contacto
                    )
                )
        except Exception as e:
            logger.error(f"Error creating patrocinador: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
    async def get_all(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_PATROCINADORES)
            if not result:
                return error_response(
                    message=PATROCINADOR_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            logger.info(f"Patrocinadores found: {result}")
            return success_response(
                data=[PatrocinadorDomain(**row) for row in result],
                message=PATROCINADOR_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error in get_all_patrosinadores: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    