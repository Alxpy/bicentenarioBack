import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.categoriaNoticia_repository_abstract import ICategoriaNoticiaRepository
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.categoriaNoticia_queries import *

class CategoriaNoticiaRepository(ICategoriaNoticiaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    async def get_categoria_noticia(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CATEGORIA_NOTICIA_BY_ID,(id,))
                result=cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Categoria de noticia encontrada.",
                    data=CategoriaNoticiaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

        
    async def get_all_categorias_noticia(self) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_CATEGORIAS_NOTICIA)
                result=cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NO_CATEGORIAS_NOTICIA_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Categorias de noticia encontradas.",
                    data=[CategoriaNoticiaDomain(**categoria) for categoria in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

    async def create_categoria_noticia(self, categoria_noticia: CategoriaNoticiaDTO) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_CATEGORIA_NOTICIA,(categoria_noticia.nombre_categoria,))
                conn.commit()
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=CATEGORIA_NOTICIA_CREATED_MSG
                )
        except mysql.connector.Error as e:
            if e.errno==1062:
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    success=False,
                    message=CATEGORIA_NOTICIA_EXISTS_MSG
                )
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_categoria_noticia(self, id: int, categoria_noticia: CategoriaNoticiaDomain) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_CATEGORIA_NOTICIA,(categoria_noticia.nombre_categoria,id))
                if cursor.rowcount==0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG
                    )
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIA_NOTICIA_UPDATED_MSG
                )
        except mysql.connector.Error as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

            
    async def delete_categoria_noticia(self, id: int) -> Response:
        conn=None
        try:
            conn=self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_CATEGORIA_NOTICIA_BY_ID,(id,))
                if cursor.rowcount==0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG
                    )
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIA_NOTICIA_DELETED_MSG
                )
        except mysql.connector.Error as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

    
    