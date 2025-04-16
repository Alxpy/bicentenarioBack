import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.multimedia_historia_respository_abstract import IMultimediaHistoriaRepository
from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain
from src.presentation.dto.multimedia_historia_dto import *
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_historia_queries import *

class MultimediaHistoriaRepository(IMultimediaHistoriaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool

    async def get_all_multimedia_historia(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_MULTIMEDIA_HISTORIA)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia historia encontrada.",
                    data=[MultimediaDatosHistoriaDTO(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_multimedia_historia_by_id_historia(self, id_historia: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_MULTIMEDIA_HISTORIA_BY_ID_HISTORIA, (id_historia,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia historia encontrada.",
                    data=[MultimediaDatosHistoriaDTO(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_multimedia_historia(self, multimedia_historia: MultimediaHistoriaDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_MULTIMEDIA_HISTORIA, (multimedia_historia.id_multimedia, multimedia_historia.id_historia))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message="Multimedia historia creada.",
                    data=multimedia_historia
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_multimedia_historia(self, id_historia: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_MULTIMEDIA_HISTORIA, (id_historia,))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia historia eliminada."
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
