import mysql.connector
import logging
from mysql.connector import pooling, IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.categoriaNoticia_repository_abstract import ICategoriaNoticiaRepository
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.categoriaNoticia_queries import *

logger = logging.getLogger(__name__)

class CategoriaNoticiaRepository(ICategoriaNoticiaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")

    async def _execute_query_all(self, query: str, params: tuple = None) -> Optional[List[dict]]:
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
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")

    async def get_categoria_noticia(self, id: int) -> Response:
        """Obtiene una categoría de noticia por su ID"""
        try:
            result = await self._execute_query(GET_CATEGORIA_NOTICIA_BY_ID, (id,))
            
            if not result:
                logger.info(f"Categoría de noticia no encontrada con ID: {id}")
                return error_response(
                    message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Categoría de noticia encontrada ID: {id}")
            return success_response(
                data=CategoriaNoticiaDomain(**result),
                message=CATEGORIA_NOTICIA_FOUND_MSG
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo categoría de noticia ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_categorias_noticia(self) -> Response:
        """Obtiene todas las categorías de noticia"""
        try:
            result = await self._execute_query_all(GET_ALL_CATEGORIAS_NOTICIA)
            
            logger.info(f"Encontradas {len(result) if result else 0} categorías de noticia")
            return success_response(
                data=[CategoriaNoticiaDomain(**categoria) for categoria in result] if result else [],
                message=CATEGORIAS_NOTICIA_FOUND_MSG if result else NO_CATEGORIAS_NOTICIA_MSG
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo categorías de noticia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_categoria_noticia(self, categoria_noticia: CategoriaNoticiaDTO) -> Response:
        """Crea una nueva categoría de noticia"""
        try:
            rowcount = await self._execute_update(
                CREATE_CATEGORIA_NOTICIA,
                (categoria_noticia.nombre_categoria,)
            )
            
            logger.info(f"Categoría de noticia creada: {categoria_noticia.nombre_categoria}")
            return success_response(
                message=CATEGORIA_NOTICIA_CREATED_MSG,
                status=HTTP_201_CREATED
            )
            
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear categoría: {str(e)}")
            return error_response(
                message=CATEGORIA_NOTICIA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando categoría de noticia: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_categoria_noticia(self, id: int, categoria_noticia: CategoriaNoticiaDomain) -> Response:
        """Actualiza una categoría de noticia existente"""
        try:
            rowcount = await self._execute_update(
                UPDATE_CATEGORIA_NOTICIA,
                (categoria_noticia.nombre_categoria, id)
            )
            
            if rowcount == 0:
                logger.info(f"Intento de actualizar categoría no existente ID: {id}")
                return error_response(
                    message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Categoría de noticia actualizada ID: {id}")
            return success_response(
                message=CATEGORIA_NOTICIA_UPDATED_MSG
            )
            
        except Exception as e:
            logger.error(f"Error actualizando categoría de noticia ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_categoria_noticia(self, id: int) -> Response:
        """Elimina una categoría de noticia"""
        try:
            rowcount = await self._execute_update(DELETE_CATEGORIA_NOTICIA_BY_ID, (id,))
            
            if rowcount == 0:
                logger.info(f"Intento de eliminar categoría no existente ID: {id}")
                return error_response(
                    message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Categoría de noticia eliminada ID: {id}")
            return success_response(
                message=CATEGORIA_NOTICIA_DELETED_MSG
            )
            
        except Exception as e:
            logger.error(f"Error eliminando categoría de noticia ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )