import mysql.connector
import logging
from typing import List
from mysql.connector import pooling, IntegrityError

from src.core.abstractions.infrastructure.repository.noticia_repository_abstract import INoticiaRepository
from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.dto.noticia_dto import NoticiaDTO
from src.presentation.responses.response_factory import Response,success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.noticia_queries import *

logger = logging.getLogger(__name__)

class NoticiaRepository(INoticiaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None) -> List[dict]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        finally:
            if self.connection:
             self.connection.close()

    async def _execute_query_all(self, query: str, params: tuple = None) -> List[dict]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        finally:
            if self.connection:
             self.connection.close()

    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización y retorna el rowcount"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        finally:
            if self.connection:
             self.connection.close()

    async def get_all_noticias(self) -> Response:
        try:
            result = await self._execute_query_all(GET_ALL_NOTICIAS)
            if not result:
                return error_response(
                    message=NO_NOTICIA_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[NoticiaDomain(**row) for row in result],
                message=NOTICIAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error en get_all_noticias: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_noticia_by_id(self, id: int) -> Response:
        try:
            result = await self._execute_query(GET_NOTICIA_BY_ID, (id,))
            if not result:
                return error_response(
                    message=NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=NoticiaDomain(**result),
                message=NOTICIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error en get_noticia_by_id: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_noticia_by_fecha(self, fecha: str) -> Response:
        try:
            result = await self._execute_query_all(GET_NOTICIA_BY_FECHA, (fecha,))
            if not result:
                return error_response(
                    message=NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[NoticiaDomain(**row) for row in result],
                message=NOTICIAS_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error en get_noticia_by_fecha: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_noticia_by_categoria(self, nomCategoria: str) -> Response:
        try:
            result = await self._execute_query_all(GET_NOTICIA_BY_CATEGORIA, (nomCategoria,))
            if not result:
                return error_response(
                    message=NO_FECHA_PUBLICACION_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=[NoticiaDomain(**row) for row in result],
                message=FECHA_PUBLICACION_EXISTS_MSG
            )
        except Exception as e:
            logger.error(f"Error en get_noticia_by_categoria: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_noticia_by_title(self, title: str) -> Response:
        try:
            result = await self._execute_query(GET_NOTICIA_BY_TITLE, (title,))
            if not result:
                return error_response(
                    message=NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                data=NoticiaDomain(**result),
                message=NOTICIA_FOUND_MSG
            )
        except Exception as e:
            logger.error(f"Error en get_noticia_by_title: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_noticia(self, noticia: NoticiaDTO) -> Response:
        try:
            params = (
                noticia.titulo,
                noticia.resumen,
                noticia.contenido,
                noticia.imagen,
                noticia.id_Categoria,
                noticia.id_usuario,
                noticia.fecha_publicacion
            )
            await self._execute_update(CREATE_NOTICIA, params)
            return success_response(
                message=NOTICIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
        except IntegrityError:
            return error_response(
                message=NOTICIA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error en create_noticia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_noticia(self, id: int, noticia: NoticiaDomain) -> Response:
        try:
            params = (
                noticia.titulo,
                noticia.resumen,
                noticia.contenido,
                noticia.imagen,
                noticia.id_Categoria,
                noticia.fecha_publicacion,
                id
            )
            rowcount = await self._execute_update(UPDATE_NOTICIA, params)
            if rowcount == 0:
                return error_response(
                    message=NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=NOTICIA_UPDATED_MSG
            )
        except Exception as e:
            logger.error(f"Error en update_noticia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_noticia(self, id: int) -> Response:
        try:
            rowcount = await self._execute_update(DELETE_NOTICIA, (id,))
            if rowcount == 0:
                return error_response(
                    message=NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            return success_response(
                message=NOTICIA_DELETED_MSG
            )
        except Exception as e:
            logger.error(f"Error en delete_noticia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )