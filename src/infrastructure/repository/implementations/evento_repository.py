import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.evento_repository_abstract import IEventoRepository
from src.core.models.evento_domain import EventoDomain
from src.presentation.dto.evento_dto import EventoDTO, EventoPostDTO, EventoUpdateDTO
from src.resources.responses.response import Response
from src.presentation.responses.response_factory import success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.evento_queries import *

logger = logging.getLogger(__name__)

class EventoRepository(IEventoRepository):
    def __init__(self, connection) -> None:
        self.connection = connection

    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
        
    async def _execute_query_all(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
    
    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización y retorna el rowcount"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")
    

    async def get_all_eventos(self) -> Response:
        try:
            result = await self._execute_query(GET_ALL_EVENTO, fetch_all=True)
            if not result:
                return error_response(
                    message=EVENTO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[EventoDomain(**row) for row in result],
                message=EVENTOS_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting all eventos: {str(e)}")
            return error_response(
                message=EVENTO_NOT_FOUND_MSG,
                status=HTTP_404_NOT_FOUND
            )
        
    async def get_evento_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_ID, (id,))
            if not result:
                return error_response(
                    message=EVENTO_BY_ID_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    async def get_evento_by_nombre(self, nombre: str) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_NOMBRE, (nombre,))
            if not result:
                return error_response(
                    message=EVENTO_BY_NOMBRE_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by nombre: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_evento_by_fecha(self, fecha: str) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_FECHA, (fecha,))
            if not result:
                return error_response(
                    message=EVENTO_BY_FECHA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by fecha: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_evento_by_tipo(self, tipo: str) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_TIPO, (tipo,))
            if not result:
                return error_response(
                    message=EVENTO_BY_TIPO_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by tipo: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_evento_by_ubicacion(self, ubicacion: str) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_UBICACION, (ubicacion,))
            if not result:
                return error_response(
                    message=EVENTO_BY_UBICACION_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by ubicacion: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def get_evento_by_organizador(self, organizador: str) -> Response:
        try:
            result = await self._execute_query(GET_EVENTO_BY_ORGANIZADOR, (organizador,))
            if not result:
                return error_response(
                    message=EVENTO_BY_ORGANIZADOR_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=EventoDomain(**result),
                message=EVENTO_FOUND_MSG,
                status=HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error getting evento by organizador: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def create_evento(self, evento: EventoPostDTO) -> Response:
        try:
            id_ubicacion = None
            if evento.id_ubicacion!=0:
                id_ubicacion = evento.id_ubicacion
            
                
            
            result = await self._execute_update(CREATE_EVENTO, (
                evento.nombre,
                evento.descripcion,
                evento.imagen,
                evento.fecha_inicio,
                evento.fecha_fin,              
                evento.id_tipo_evento,
                id_ubicacion,
                evento.id_usuario,
                evento.id_organizador,
                evento.categoria,
                evento.enlace,
                evento.precio
            ))
            if result == 0:
                return error_response(
                    message=EVENTO_NOT_CREATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            logger.info(f"Evento created with id:  {result}")
            
            
            return success_response(
                message=EVENTO_CREATED_MSG,
                status=HTTP_201_CREATED,
                data=EventoDomain(
                    id=result,
                    nombre=evento.nombre,
                    descripcion=evento.descripcion,
                    imagen=evento.imagen,
                    fecha_inicio=evento.fecha_inicio,
                    fecha_fin=evento.fecha_fin,
                    id_tipo_evento=evento.id_tipo_evento,
                    id_ubicacion=evento.id_ubicacion,
                    id_usuario=evento.id_usuario,
                    id_organizador=evento.id_organizador
                )
                
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in create_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    async def update_evento(self, id: int, evento: EventoUpdateDTO) -> Response:
        try:
            result = await self._execute_update(UPDATE_EVENTO, (
                evento.nombre,
                evento.descripcion,
                evento.imagen,
                evento.fecha_inicio,
                evento.fecha_fin,              
                evento.id_tipo_evento,
                evento.id_ubicacion,  
                evento.id_usuario,
                id
            ))
            if result == 0:
                return error_response(
                    message=EVENTO_NOT_UPDATED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=EVENTO_UPDATED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in update_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def delete_evento(self, id: int) -> Response:
        try:
            result = await self._execute_update(DELETE_EVENTO, (id,))
            if result == 0:
                return error_response(
                    message=EVENTO_NOT_DELETED_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
            return success_response(
                message=EVENTO_DELETED_MSG,
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            logger.error(f"Integrity error in delete_evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting evento: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        



