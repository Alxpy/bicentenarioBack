import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.cultura_repository_abstract import ICulturaRepository
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.cultura_queries import *

class CulturaRepository(ICulturaRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    async def get_all_culturas(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_CULTARAS)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_CULTURAS_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURAS_FOUND_MSG,
                    data=[CulturaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_cultura_by_id(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CULTURA_BY_ID_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURA_BY_ID_MSG,
                    data=CulturaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_cultura_by_nombre(self, nombre: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_NOMBRE, (nombre,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CULTURA_BY_NOMBRE_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURA_BY_NOMBRE_MSG,
                    data=CulturaDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_cultura_by_ubicacion(self, ubicacion: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_UBICACION, (ubicacion,))
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=CULTURA_BY_UBICACION_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURA_BY_UBICACION_MSG,
                    data=[CulturaDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def create_cultura(self, cultura: CulturaDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(CREATE_CULTURA, (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=CULTURA_CREATED_MSG
                )
        except Error as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_cultura(self, id: int, cultura: CulturaDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_CULTURA, (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion, id))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURA_UPDATED_MSG
                )
        except Error as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_cultura(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor() as cursor:
                cursor.execute(DELETE_CULTURA, (id,))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=CULTURA_DELETED_MSG
                )
        except Error as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    