import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.tipoDocumento_repository_abstract import ITipoDocumentoRepository
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO
from src.presentation.responses.response_factory import Response,success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.tipoDocumento_queries import *

logger = logging.getLogger(__name__)

class TipoDocumentoRepository(ITipoDocumentoRepository):
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

    async def get_tipo_documento(self, id: int) -> Response:
        """Obtiene un tipo de documento por su ID"""
        try:
            result = await self._execute_query(GET_TIPO_DOCUMENTO_BY_ID, (id,))
            if not result:
                logger.info(f"Tipo documento no encontrado con ID: {id}")
                return error_response(
                    message=TIPO_DOCUMENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=TipoDocumentoDomain(**result),
                message=TIPO_DOCUMENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo tipo documento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_tipos_documento(self) -> Response:
        """Obtiene todos los tipos de documento"""
        try:
            result = await self._execute_query_all(GET_ALL_TIPOS_DOCUMENTO)
            if not result:
                logger.info("No se encontraron tipos de documento")
                return error_response(
                    message=TIPO_DOCUMENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[TipoDocumentoDomain(**row) for row in result],
                message=TIPOS_DOCUMENTO_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo tipos de documento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_tipo_documento(self, tipo_documento: TipoDocumentoDTO) -> Response:
        """Crea un nuevo tipo de documento"""
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_TIPO_DOCUMENTO, (tipo_documento.tipo,))
                conn.commit()
                return success_response(
                    data=TipoDocumentoDomain(
                        id_tipo=cursor.lastrowid,
                        tipo=tipo_documento.tipo
                    ),
                    message=TIPO_DOCUMENTO_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear tipo documento: {str(e)}")
            return error_response(
                message=TIPO_DOCUMENTO_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando tipo documento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            if conn:
                conn.close()

    async def update_tipo_documento(self, id: int, tipo_documento: TipoDocumentoDomain) -> Response:
        """Actualiza un tipo de documento existente"""
        try:
            rowcount = await self._execute_update(
                UPDATE_TIPO_DOCUMENTO,
                (tipo_documento.tipo, id)
            )
            if rowcount == 0:
                logger.info(f"Intento de actualizar tipo documento no existente ID: {id}")
                return error_response(
                    message=TIPO_DOCUMENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=TIPO_DOCUMENTO_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error actualizando tipo documento ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_tipo_documento(self, id: int) -> Response:
        """Elimina un tipo de documento"""
        try:
            rowcount = await self._execute_update(DELETE_TIPO_DOCUMENTO, (id,))
            if rowcount == 0:
                logger.info(f"Intento de eliminar tipo documento no existente ID: {id}")
                return error_response(
                    message=TIPO_DOCUMENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=TIPO_DOCUMENTO_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error eliminando tipo documento ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )