import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.ubicacion_repository_abstract import IUbicacionRepository
from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.dto.ubicacion_dto import UbicacionDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.ubicacion_queries import *

class UbicacionRepository(IUbicacionRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool
    
    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    async def get_all_ubicaciones(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_UBICACIONES)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_UBICACION_MDG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=UBICACIONES_FOUND_MSG,
                    data=[UbicacionDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_ubicacion_by_id(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_UBICACION_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NO_UBICACION_MDG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=UBICACION_FOUND_MSG,
                    data=UbicacionDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def get_ubicacion_by_name(self, nombre: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_UBICACION_BY_NAME, (nombre,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NO_UBICACION_MDG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=UBICACION_FOUND_MSG,
                    data=UbicacionDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    

    async def create_ubicacion(self, ubicacion: UbicacionDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(CREATE_UBICACION, 
                    (ubicacion.nombre, 
                     ubicacion.latitud, 
                     ubicacion.longitud, 
                     ubicacion.imagen,
                     ubicacion.descripcion
                     ))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=UBICACION_CREATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def update_ubicacion(self, id: int, ubicacion: UbicacionDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(UPDATE_UBICACION, (ubicacion.nombre, 
                                                ubicacion.latitud,
                                                ubicacion.longitud,
                                                ubicacion.imagen,
                                                ubicacion.descripcion,  
                                                id))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=UBICACCION_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

    async def delete_ubicacion(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(DELETE_UBICACION, (id,))
                conn.commit()
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=UBICACION_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )