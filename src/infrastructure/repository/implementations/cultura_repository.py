import mysql.connector
from mysql.connector import pooling
from typing import Optional

import logging
from mysql.connector import Error, IntegrityError
from typing import List, Optional


from src.core.abstractions.infrastructure.repository.cultura_repository_abstract import ICulturaRepository
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO
from src.presentation.responses.response_factory import Response,success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.cultura_queries import *

logger = logging.getLogger(__name__)

class CulturaRepository(ICulturaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        """Ejecuta una consulta SQL y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Error as e:
            logger.error(f"Error en consulta SQL: {str(e)}")

    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización y retorna el número de filas afectadas"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        except Error as e:
            logger.error(f"Error en actualización SQL: {str(e)}")

    async def get_all_culturas(self) -> Response:
        """Obtiene todas las culturas registradas"""
        try:
            result = await self._execute_query(GET_ALL_CULTARAS, fetch_all=True)
            
            if not result:
                logger.info("No se encontraron culturas registradas")
                return error_response(
                    message=NO_CULTURAS_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Se encontraron {len(result)} culturas")
            return success_response(
                data=[CulturaDomain(**row) for row in result],
                message=CULTURAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error al obtener todas las culturas: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_id(self, id: int) -> Response:
        """Obtiene una cultura por su ID"""
        try:
            result = await self._execute_query(GET_CULTURA_BY_ID, (id,))
            
            if not result:
                logger.info(f"Cultura no encontrada con ID: {id}")
                return error_response(
                    message=CULTURA_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Cultura encontrada con ID: {id}")
            return success_response(
                data=CulturaDomain(**result),
                message=CULTURA_BY_ID_MSG
            )
        except Exception as e:
            logger.error(f"Error al obtener cultura por ID {id}: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_nombre(self, nombre: str) -> Response:
        """Obtiene una cultura por su nombre"""
        try:
            result = await self._execute_query(GET_CULTURA_BY_NOMBRE, (nombre,))
            
            logger.info(f"Búsqueda de cultura por nombre: {nombre} - {'Encontrada' if result else 'No encontrada'}")
            return success_response(
                data=CulturaDomain(**result) if result else None,
                message=CULTURA_BY_NOMBRE_MSG if result else CULTURA_BY_NOMBRE_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error al obtener cultura por nombre {nombre}: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_ubicacion(self, ubicacion: str) -> Response:
        """Obtiene culturas por ubicación"""
        try:
            result = await self._execute_query(GET_CULTURA_BY_UBICACION, (ubicacion,), fetch_all=True)
            
            logger.info(f"Se encontraron {len(result) if result else 0} culturas para la ubicación: {ubicacion}")
            return success_response(
                data=[CulturaDomain(**row) for row in result] if result else [],
                message=CULTURA_BY_UBICACION_MSG if result else CULTURA_BY_UBICACION_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error al obtener culturas por ubicación {ubicacion}: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_cultura(self, cultura: CulturaDTO) -> Response:
        """Crea una nueva cultura"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    CREATE_CULTURA, 
                    (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion)
                )
                self.connection.commit()
                
                logger.info(f"Cultura creada exitosamente: {cultura.nombre}")
                return success_response(
                    message=CULTURA_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear cultura: {str(e)}")
            return error_response(
                message=CULTURA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error al crear cultura: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_cultura(self, id: int, cultura: CulturaDomain) -> Response:
        """Actualiza una cultura existente"""
        try:
            rowcount = await self._execute_update(
                UPDATE_CULTURA,
                (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion, id)
            )
            
            if rowcount == 0:
                logger.info(f"Intento de actualizar cultura no existente ID: {id}")
                return error_response(
                    message=CULTURA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            logger.info(f"Cultura actualizada exitosamente ID: {id}")
            return success_response(
                message=CULTURA_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error al actualizar cultura ID {id}: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR

            )

    async def delete_cultura(self, id: int) -> Response:
        """Elimina una cultura"""
        try:
            rowcount = await self._execute_update(DELETE_CULTURA, (id,))
            
            if rowcount == 0:
                logger.info(f"Intento de eliminar cultura no existente ID: {id}")
                return error_response(
                    message=CULTURA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Cultura eliminada exitosamente ID: {id}")
            return success_response(
                message=CULTURA_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error al eliminar cultura ID {id}: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )