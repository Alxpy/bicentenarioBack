import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.multimedia_repository_abstract import IMultimediaRepository
from src.core.models.multimedia_domain import MultimediaDomain
from src.presentation.dto.multimedia_dto import MultimediaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_queries import *

class MultimediaRepository(IMultimediaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    async def get_all_multimedia(self) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_MULTIMEDIA)
                result=cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia encontrada.",
                    data=[MultimediaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_multimedia_by_id(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_MULTIMEDIA_BY_ID, (id,))
                result=cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_BY_ID_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=MULTIMEDIA_BY_ID_MSG,
                    data=MultimediaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_multimedia(self, multimedia: MultimediaDomain) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(CREATE_MULTIMEDIA, (multimedia.enlace, multimedia.tipo))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_400_BAD_REQUEST,
                        success=False,
                        message=MULTIMEDIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=MULTIMEDIA_CREATED_MSG,
                    data=multimedia
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_multimedia(self, id: int, multimedia: MultimediaDomain) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(UPDATE_MULTIMEDIA, (multimedia.enlace, multimedia.tipo, id))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=MULTIMEDIA_UPDATED_MSG,
                    data=multimedia
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_multimedia(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(DELETE_MULTIMEDIA, (id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=MULTIMEDIA_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )