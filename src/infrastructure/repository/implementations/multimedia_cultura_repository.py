import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.multimedia_cultura_repository_abstract import IMultimediaCulturaRepository
from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain
from src.presentation.dto.multimedia_cultura_dto import *
from src.resources.responses.response import Response   
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.multimedia_cultura_queries import *

class MultimediaCulturaRepository(IMultimediaCulturaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool


    async def get_all_multimedia_cultura(self) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_MULTIMEDIA_CULTURA)
                result=cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_CULTURA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia cultura encontrada.",
                    data=[MultimediaDatosCulturaDTO(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_multimedia_cultura_by_id_cultura(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_MULTIMEDIA_CULTURA_BY_ID_CULTURA, (id,))
                result=cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=MULTIMEDIA_CULTURA_NOT_FOUND_MSG
                    )            
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia cultura encontrada.",
                    data=[MultimediaDatosCulturaDTO(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_multimedia_cultura(self, multimedia_cultura: MultimediaCulturaDomain) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(CREATE_MULTIMEDIA_CULTURA, (multimedia_cultura.id_multimedia,multimedia_cultura.id_cultura))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message="Multimedia cultura creada.",
                    data=MultimediaCulturaDomain(**multimedia_cultura.dict())
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_multimedia_cultura(self, id_cultura: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(DELETE_MULTIMEDIA_CULTURA, (id_cultura,))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Multimedia cultura eliminada."
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
