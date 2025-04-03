import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.biblioteca_repository_abstract import IBibliotecaRepository
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.biblioteca_queries import *

class BibliotecaRepository(IBibliotecaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool

    async def get_all_bibliotecas(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_BIBLIOTECAS)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_BIBLIOTECA_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECAS_FOUND_MSG,
                    data=[BibliotecaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

    async def get_biblioteca_by_id(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECA_FOUND_MSG,
                    data=BibliotecaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_biblioteca_by_title(self, title: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_TITLE, (title,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECA_FOUND_MSG,
                    data=BibliotecaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_biblioteca_by_categoria(self, categoria: str) -> Response:
        conn= None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_CATEGORIA, (categoria,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECAS_FOUND_MSG,
                    data=[BibliotecaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_biblioteca_by_autor(self, autor: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_AUTOR, (autor,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECAS_FOUND_MSG,
                    data=[BibliotecaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_biblioteca_by_fecha(self, fecha: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_FECHA, (fecha,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECAS_FOUND_MSG,
                    data=[BibliotecaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_biblioteca(self, biblioteca_dto: BibliotecaDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_BIBLIOTECA, (
                    biblioteca_dto.titulo,
                    biblioteca_dto.autor,
                    biblioteca_dto.imagen,
                    biblioteca_dto.fecha_publicacion,
                    biblioteca_dto.edicion,
                    biblioteca_dto.id_tipo,
                    biblioteca_dto.fuente,
                    biblioteca_dto.enlace
                ))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=BIBLIOTECA_CREATED_MSG
                )
        except mysql.connector.IntegrityError:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                success=False,
                message=BIBLIOTECA_EXIST_MSG
            )    
        
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_biblioteca(self, id: int, biblioteca_dto: BibliotecaDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_BIBLIOTECA, (
                    biblioteca_dto.titulo,
                    biblioteca_dto.autor,
                    biblioteca_dto.imagen,
                    biblioteca_dto.fecha_publicacion,
                    biblioteca_dto.edicion,
                    biblioteca_dto.id_tipo,
                    biblioteca_dto.fuente,
                    biblioteca_dto.enlace,
                    id
                ))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECA_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_biblioteca(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_BIBLIOTECA, (id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=BIBLIOTECA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=BIBLIOTECA_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
