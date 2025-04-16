import mysql.connector
from mysql.connector import pooling
from typing import Optional
import logging
logger = logging.getLogger(__name__)
from src.core.abstractions.infrastructure.repository.biblioteca_repository_abstract import IBibliotecaRepository
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO
from src.presentation.responses.response_factory import success_response, error_response
from src.presentation.responses.base_response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.biblioteca_queries import *

class BibliotecaRepository(IBibliotecaRepository):
    def __init__(self, connection):
        self.self.connectionection = connection

    async def get_all_bibliotecas(self) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_BIBLIOTECAS)
                result = cursor.fetchall()
                
                if not result:
                    return error_response(
                        message=NO_BIBLIOTECA_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    data=[BibliotecaDomain(**row) for row in result],
                    message=BIBLIOTECAS_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_all_bibliotecas: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_id(self, id: int) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return error_response(
                        message=BIBLIOTECA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    data=BibliotecaDomain(**result),
                    message=BIBLIOTECA_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_biblioteca_by_id: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_title(self, title: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_TITLE, (title,))
                result = cursor.fetchone()
                
                return success_response(
                    data=BibliotecaDomain(**result) if result else None,
                    message=BIBLIOTECA_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_biblioteca_by_title: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_categoria(self, categoria: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_CATEGORIA, (categoria,))
                result = cursor.fetchall()
                
                return success_response(
                    data=[BibliotecaDomain(**row) for row in result] if result else [],
                    message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_biblioteca_by_categoria: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_autor(self, autor: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_AUTOR, (autor,))
                result = cursor.fetchall()
                
                return success_response(
                    data=[BibliotecaDomain(**row) for row in result] if result else [],
                    message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_biblioteca_by_autor: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_biblioteca_by_fecha(self, fecha: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_BIBLIOTECA_BY_FECHA, (fecha,))
                result = cursor.fetchall()
                
                return success_response(
                    data=[BibliotecaDomain(**row) for row in result] if result else [],
                    message=BIBLIOTECAS_FOUND_MSG if result else BIBLIOTECA_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_biblioteca_by_fecha: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_biblioteca(self, biblioteca_dto: BibliotecaDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_BIBLIOTECA, (
                    biblioteca_dto.titulo,
                    biblioteca_dto.autor,
                    biblioteca_dto.imagen,
                    biblioteca_dto.fecha_publicacion,
                    biblioteca_dto.edicion,
                    biblioteca_dto.id_usuario,
                    biblioteca_dto.id_tipo,
                    biblioteca_dto.fuente,
                    biblioteca_dto.enlace
                ))
                self.connection.commit()
                
                return success_response(
                    message=BIBLIOTECA_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
                
        except mysql.self.connectionector.IntegrityError as e:
            logger.error("Error de integridad en create_biblioteca: %s", e)
            return error_response(
                message=BIBLIOTECA_EXIST_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error en create_biblioteca: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_biblioteca(self, id: int, biblioteca_dto: BibliotecaDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
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
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=BIBLIOTECA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=BIBLIOTECA_UPDATED_MSG
                )
                
        except Exception as e:
            logger.error("Error en update_biblioteca: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_biblioteca(self, id: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DELETE_BIBLIOTECA, (id,))
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=BIBLIOTECA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=BIBLIOTECA_DELETED_MSG
                )
                
        except Exception as e:
            logger.error("Error en delete_biblioteca: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
