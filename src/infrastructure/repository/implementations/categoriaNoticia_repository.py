import mysql.connector
from mysql.connector import pooling
import logging
logger = logging.getLogger(__name__)

from src.core.abstractions.infrastructure.repository.categoriaNoticia_repository_abstract import ICategoriaNoticiaRepository
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response

from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.categoriaNoticia_queries import *

class CategoriaNoticiaRepository(ICategoriaNoticiaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection
    

    async def get_categoria_noticia(self, id: int) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CATEGORIA_NOTICIA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return error_response(
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    data=CategoriaNoticiaDomain(**result),
                    message=CATEGORIA_NOTICIA_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_categoria_noticia: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_categorias_noticia(self) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_CATEGORIAS_NOTICIA)
                result = cursor.fetchall()
                
                return success_response(
                    data=[CategoriaNoticiaDomain(**categoria) for categoria in result] if result else [],
                    message=CATEGORIAS_NOTICIA_FOUND_MSG if result else NO_CATEGORIAS_NOTICIA_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_all_categorias_noticia: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


    async def create_categoria_noticia(self, categoria_noticia: CategoriaNoticiaDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    CREATE_CATEGORIA_NOTICIA,
                    (categoria_noticia.nombre_categoria,)
                )
                self.connection.commit()
                
                return success_response(
                    message=CATEGORIA_NOTICIA_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
                
        except mysql.connector.IntegrityError as e:
            logger.error("Error de integridad en create_categoria_noticia: %s", e)
            return error_response(
                message=CATEGORIA_NOTICIA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error en create_categoria_noticia: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


    async def update_categoria_noticia(self, id: int, categoria_noticia: CategoriaNoticiaDomain) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    UPDATE_CATEGORIA_NOTICIA,
                    (categoria_noticia.nombre_categoria, id)
                )
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=CATEGORIA_NOTICIA_UPDATED_MSG
                )
                
        except Exception as e:
            logger.error("Error en update_categoria_noticia: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_categoria_noticia(self, id: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DELETE_CATEGORIA_NOTICIA_BY_ID, (id,))
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=CATEGORIA_NOTICIA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=CATEGORIA_NOTICIA_DELETED_MSG
                )
                
        except Exception as e:
            logger.error("Error en delete_categoria_noticia: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )