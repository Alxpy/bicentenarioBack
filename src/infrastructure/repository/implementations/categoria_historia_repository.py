import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.categoria_historia_repository_abstract import ICategoriaHistoriaRepository
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.categoria_historia_queries import *


class CategoriaHistoriaRepository(ICategoriaHistoriaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool

    def _get_connection(self):
        return self.connection_pool
    
    async def get_categoria_historia(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CATEGORIA_HISTORIA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIA_HISTORIA_FOUND_MSG,
                    data=CategoriaHistoriaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_all_categorias_historia(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_CATEGORIA_HISTORIA)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIAS_HISTORIA_FOUND_MSG,
                    data=[CategoriaHistoriaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_categoria_historia(self, categoria_historia: CategoriaHistoriaDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_CATEGORIA_HISTORIA, (categoria_historia.nombre, categoria_historia.descripcion))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_400_BAD_REQUEST,
                        success=False,
                        message=CATEGORIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=CATEGORIA_HISTORIA_CREATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_categoria_historia(self, id: int, categoria_historia: CategoriaHistoriaDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_CATEGORIA_HISTORIA, (categoria_historia.nombre, categoria_historia.descripcion, id))
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIA_HISTORIA_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_categoria_historia(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_CATEGORIA_HISTORIA, (id,))
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CATEGORIA_HISTORIA_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CATEGORIA_HISTORIA_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    