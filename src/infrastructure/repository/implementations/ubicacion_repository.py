import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.ubicacion_repository_abstract import IUbicacionRepository
from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.dto.ubicacion_dto import UbicacionDTO
from src.presentation.responses.response_factory import Response,success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.ubicacion_queries import *

logger = logging.getLogger(__name__)

class UbicacionRepository(IUbicacionRepository):
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
    

    async def get_all_ubicaciones(self) -> Response:
        """Obtiene todas las ubicaciones registradas"""
        try:
            result = await self._execute_query_all(GET_ALL_UBICACIONES)
            if not result:
                logger.info("No se encontraron ubicaciones")
                return error_response(
                    message=NO_UBICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[UbicacionDomain(**row) for row in result],
                message=UBICACIONES_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo ubicaciones: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_ubicacion_by_id(self, id: int) -> Response:
        """Obtiene una ubicación por su ID"""
        try:
            result = await self._execute_query(GET_UBICACION_BY_ID, (id,))
            if not result:
                logger.info(f"Ubicación no encontrada con ID: {id}")
                return error_response(
                    message=NO_UBICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=UbicacionDomain(**result),
                message=UBICACION_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo ubicación ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_ubicacion_by_name(self, nombre: str) -> Response:
        """Obtiene una ubicación por su nombre"""
        try:
            result = await self._execute_query(GET_UBICACION_BY_NAME, (nombre,))
            if not result:
                logger.info(f"Ubicación no encontrada con nombre: {nombre}")
                return error_response(
                    message=NO_UBICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=UbicacionDomain(**result),
                message=UBICACION_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo ubicación por nombre {nombre}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_ubicacion(self, ubicacion: UbicacionDTO) -> Response:
        """Crea una nueva ubicación"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_UBICACION, (
                    ubicacion.nombre,
                    ubicacion.latitud,
                    ubicacion.longitud,
                    ubicacion.imagen,
                    ubicacion.descripcion
                ))
                self.connection.commit()
                return success_response(
                    message=UBICACION_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear ubicación: {str(e)}")
            return error_response(
                message=UBICACION_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando ubicación: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_ubicacion(self, id: int, ubicacion: UbicacionDomain) -> Response:
        """Actualiza una ubicación existente"""
        try:
            rowcount = await self._execute_update(
                UPDATE_UBICACION,
                (
                    ubicacion.nombre,
                    ubicacion.latitud,
                    ubicacion.longitud,
                    ubicacion.imagen,
                    ubicacion.descripcion,
                    id
                )
            )
            if rowcount == 0:
                logger.info(f"Intento de actualizar ubicación no existente ID: {id}")
                return error_response(
                    message=NO_UBICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=UBICACION_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error actualizando ubicación ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_ubicacion(self, id: int) -> Response:
        """Elimina una ubicación"""
        try:
            rowcount = await self._execute_update(DELETE_UBICACION, (id,))
            if rowcount == 0:
                logger.info(f"Intento de eliminar ubicación no existente ID: {id}")
                return error_response(
                    message=NO_UBICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=UBICACION_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error eliminando ubicación ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )