import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.tipoDocumento_repository_abstract import ITipoDocumentoRepository
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.tipoDocumento_queries import *

class TipoDocumentoRepository(ITipoDocumentoRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    async def get_tipo_documento(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_TIPO_DOCUMENTO_BY_ID,(id,))
                result=cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=TIPO_DOCUMENTO_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Tipo de documento encontrado.",
                    data=TipoDocumentoDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_all_tipos_documento(self) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_TIPOS_DOCUMENTO)
                result=cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=TIPO_DOCUMENTO_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Tipos de documento encontrados.",
                    data=[TipoDocumentoDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_tipo_documento(self, tipo_documento: TipoDocumentoDTO) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(CREATE_TIPO_DOCUMENTO,(tipo_documento.tipo,))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message="Tipo de documento creado.",
                    data=TipoDocumentoDomain(id_tipo=cursor.lastrowid,tipo=tipo_documento.tipo)
                )
        except mysql.connector.IntegrityError as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                success=False,
                message=f"Error de integridad: {str(e)}"
            )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    async def update_tipo_documento(self, id: int, tipo_documento: TipoDocumentoDomain) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_TIPO_DOCUMENTO,(tipo_documento.tipo,id))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=TIPO_DOCUMENTO_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=TIPO_DOCUMENTO_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_tipo_documento(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_TIPO_DOCUMENTO,(id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=TIPO_DOCUMENTO_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=TIPO_DOCUMENTO_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )