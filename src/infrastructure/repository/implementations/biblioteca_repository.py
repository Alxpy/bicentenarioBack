import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.biblioteca_repository_abstract import IBibliotecaRepository
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.biblioteca_queries import *

logger = logging.getLogger(__name__)

class BibliotecaRepository(IBibliotecaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")

    async def _execute_update(self, query: str, params: tuple = None) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")

    async def get_all_bibliotecas(self) -> Response:
        """Obtiene todas las bibliotecas registradas"""
        try:
            result = await self._execute_query(GET_ALL_BIBLIOTECAS, fetch_all=True)
            if not result:
                logger.info("No se encontraron bibliotecas")
                return error_response(
                    message=NO_BIBLIOTECA_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[BibliotecaDomain(**row) for row in result],
                message=BIBLIOTECAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo bibliotecas: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_id(self, id: int) -> Response:
        """Obtiene una biblioteca por su ID"""
        try:
            result = await self._execute_query(GET_BIBLIOTECA_BY_ID, (id,))
            if not result:
                logger.info(f"Biblioteca no encontrada con ID: {id}")
                return error_response(
                    message=BIBLIOTECA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=BibliotecaDomain(**result),
                message=BIBLIOTECA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo biblioteca ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_title(self, title: str) -> Response:
        """Obtiene una biblioteca por su título"""
        try:
            result = await self._execute_query(GET_BIBLIOTECA_BY_TITLE, (title,))
            return success_response(
                data=BibliotecaDomain(**result) if result else None,
                message=BIBLIOTECA_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo biblioteca por título {title}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_categoria(self, categoria: str) -> Response:
        """Obtiene bibliotecas por categoría"""
        try:
            result = await self._execute_query(GET_BIBLIOTECA_BY_CATEGORIA, (categoria,), fetch_all=True)
            return success_response(
                data=[BibliotecaDomain(**row) for row in result] if result else [],
                message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo bibliotecas por categoría {categoria}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_autor(self, autor: str) -> Response:
        """Obtiene bibliotecas por autor"""
        try:
            result = await self._execute_query(GET_BIBLIOTECA_BY_AUTOR, (autor,), fetch_all=True)
            return success_response(
                data=[BibliotecaDomain(**row) for row in result] if result else [],
                message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo bibliotecas por autor {autor}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_fecha(self, fecha: str) -> Response:
        """Obtiene bibliotecas por fecha de publicación"""
        try:
            result = await self._execute_query(GET_BIBLIOTECA_BY_FECHA, (fecha,), fetch_all=True)
            return success_response(
                data=[BibliotecaDomain(**row) for row in result] if result else [],
                message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error obteniendo bibliotecas por fecha {fecha}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_biblioteca(self, biblioteca_dto: BibliotecaDTO) -> Response:
        """Crea una nueva biblioteca"""
        try:
            params = (
                biblioteca_dto.titulo,
                biblioteca_dto.autor,
                biblioteca_dto.imagen,
                biblioteca_dto.fecha_publicacion,
                biblioteca_dto.edicion,
                biblioteca_dto.id_usuario,
                biblioteca_dto.id_tipo,
                biblioteca_dto.fuente,
                biblioteca_dto.enlace
            )
            await self._execute_update(CREATE_BIBLIOTECA, params)
            return success_response(
                message=BIBLIOTECA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear biblioteca: {str(e)}")
            return error_response(
                message=BIBLIOTECA_EXIST_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando biblioteca: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_biblioteca(self, id: int, biblioteca_dto: BibliotecaDTO) -> Response:
        """Actualiza una biblioteca existente"""
        try:
            params = (
                biblioteca_dto.titulo,
                biblioteca_dto.autor,
                biblioteca_dto.imagen,
                biblioteca_dto.fecha_publicacion,
                biblioteca_dto.edicion,
                biblioteca_dto.id_tipo,
                biblioteca_dto.fuente,
                biblioteca_dto.enlace,
                id
            )
            rowcount = await self._execute_update(UPDATE_BIBLIOTECA, params)
            if rowcount == 0:
                logger.info(f"Intento de actualizar biblioteca no existente ID: {id}")
                return error_response(
                    message=BIBLIOTECA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=BIBLIOTECA_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error actualizando biblioteca ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_biblioteca(self, id: int) -> Response:
        """Elimina una biblioteca"""
        try:
            rowcount = await self._execute_update(DELETE_BIBLIOTECA, (id,))
            if rowcount == 0:
                logger.info(f"Intento de eliminar biblioteca no existente ID: {id}")
                return error_response(
                    message=BIBLIOTECA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=BIBLIOTECA_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error eliminando biblioteca ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )