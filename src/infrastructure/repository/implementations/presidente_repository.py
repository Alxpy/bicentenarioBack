import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.presidente_repository_abstract import IPresidenteRepository
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.dto.presidente_dto import PresidenteDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.presidente_queries import *

class PresidenteRepository(IPresidenteRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool

    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool
    
    
    async def get_all_presidentes(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_PRESIDENTES)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=NO_PRESIDENTE_MDG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PRESIDENTES_FOUND_MSG,
                    data=[PresidenteDomain(**row) for row in result]
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_presidente_by_id(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_PRESIDENTE_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=PRESIDENTE_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PRESIDENTE_FOUND_MSG,
                    data=PresidenteDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def get_presidente_by_nombre(self, nombre: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_PRESIDENTE_BY_NOMBRE, (nombre,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NO_PRESIDENTE_BY_NOMBRE_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PRESIDENTE_BY_NAMBRE_MSG,
                    data=PresidenteDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        
    async def create_presidente(self, presidente_dto: PresidenteDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(CREATE_PRESIDENTE, (
                    presidente_dto.nombre,
                    presidente_dto.apellido,
                    presidente_dto.imagen,
                    presidente_dto.inicio_periodo,
                    presidente_dto.fin_periodo,
                    presidente_dto.bibliografia,
                    presidente_dto.partido_politico,
                    presidente_dto.principales_politicas,
                    presidente_dto.id_usuario
                ))
                conn.commit()
                
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=PRESIDENTE_CREATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def update_presidente(self, id: int, presidente_dto: PresidenteDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(UPDATE_PRESIDENTE, (
                    presidente_dto.nombre,
                    presidente_dto.apellido,
                    presidente_dto.imagen,
                    presidente_dto.inicio_periodo,
                    presidente_dto.fin_periodo,
                    presidente_dto.bibliografia,
                    presidente_dto.partido_politico,
                    presidente_dto.principales_politicas,
                    presidente_dto.id_usuario,
                    id
                ))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=PRESIDENTE_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PRESIDENTE_UPDATED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
    
    async def delete_presidente(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(DELETE_PRESIDENTE, (id,))
                conn.commit()
                
                if cursor.rowcount == 0:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=PRESIDENTE_NOT_FOUND_MSG
                    )
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PRESIDENTE_DELETED_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        