import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.noticia_repository_abstract import INoticiaRepository
from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.dto.noticia_dto import NoticiaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.noticia_queries import *

class NoticiaRepository(INoticiaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool

    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    
    
    async def get_all_noticias(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_NOTICIAS)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_NOTICIA_MDG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIAS_FOUND_MSG,
                    data=[NoticiaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_noticia_by_id(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_NOTICIA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NOTICIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIA_FOUND_MSG,
                    data=NoticiaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_noticia_by_fecha(self, fecha: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_NOTICIA_BY_FECHA, (fecha,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NOTICIA_NOT_FOUND_MSG
                    )
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIAS_FOUND_MSG,
                    data=[NoticiaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_noticia_by_categoria(self, nomCategoria: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_NOTICIA_BY_CATEGORIA, (nomCategoria,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_FECHA_PUBLICACION_MSG
                    )
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=FECHA_PUBLICACION_EXISTS_MSG,
                    data=[NoticiaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_noticia_by_title(self, title: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_NOTICIA_BY_TITLE, (title,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NOTICIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIA_FOUND_MSG,
                    data=NoticiaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_noticia(self, noticia: NoticiaDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_NOTICIA, (
                    noticia.titulo,
                    noticia.resumen,
                    noticia.contenido,
                    noticia.imagen,
                    noticia.idCategoria,
                    noticia.fecha_publicacion
                ))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=NOTICIA_CREATED_MSG
                )
        except mysql.connector.IntegrityError:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                success=False,
                message=NOTICIA_EXISTS_MSG
            )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_noticia(self, id: int, noticia: NoticiaDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_NOTICIA, (
                    noticia.titulo,
                    noticia.resumen,
                    noticia.contenido,
                    noticia.imagen,
                    noticia.idCategoria,
                    noticia.fecha_publicacion,
                    id
                ))
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NOTICIA_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIA_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def delete_noticia(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_NOTICIA, (id,))
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NOTICIA_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=NOTICIA_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )