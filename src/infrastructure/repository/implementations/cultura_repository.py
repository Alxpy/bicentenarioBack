import mysql.connector
from mysql.connector import Error, IntegrityError
import logging
logger = logging.getLogger(__name__)

from src.core.abstractions.infrastructure.repository.cultura_repository_abstract import ICulturaRepository
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.cultura_queries import *

class CulturaRepository(ICulturaRepository):
    def __init__(self, connection) -> None:
        self.connection = connection
    

    async def get_all_culturas(self) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_CULTARAS)
                result = cursor.fetchall()
                
                if not result:
                    return error_response(
                        message=NO_CULTURAS_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    data=[CulturaDomain(**row) for row in result],
                    message=CULTURAS_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_all_culturas: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_id(self, id: int) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return error_response(
                        message=CULTURA_BY_ID_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    data=CulturaDomain(**result),
                    message=CULTURA_BY_ID_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_cultura_by_id: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_nombre(self, nombre: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_NOMBRE, (nombre,))
                result = cursor.fetchone()
                
                return success_response(
                    data=CulturaDomain(**result) if result else None,
                    message=CULTURA_BY_NOMBRE_MSG if result else CULTURA_BY_NOMBRE_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_cultura_by_nombre: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_cultura_by_ubicacion(self, ubicacion: str) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_CULTURA_BY_UBICACION, (ubicacion,))
                result = cursor.fetchall()
                
                return success_response(
                    data=[CulturaDomain(**row) for row in result] if result else [],
                    message=CULTURA_BY_UBICACION_MSG if result else CULTURA_BY_UBICACION_NOT_FOUND_MSG
                )
                
        except Exception as e:
            logger.error("Error en get_cultura_by_ubicacion: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


    async def create_cultura(self, cultura: CulturaDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    CREATE_CULTURA, 
                    (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion)
                )
                self.connection.commit()
                
                return success_response(
                    message=CULTURA_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
                
        except IntegrityError as e:
            logger.error("Error de integridad en create_cultura: %s", e)
            return error_response(
                message=CULTURA_EXISTS_MSG,
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Error en create_cultura: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


    async def update_cultura(self, id: int, cultura: CulturaDomain) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    UPDATE_CULTURA,
                    (cultura.nombre, cultura.imagen, cultura.descripcion, cultura.id_ubicacion, id)
                )
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=CULTURA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=CULTURA_UPDATED_MSG
                )
                
        except Exception as e:
            logger.error("Error en update_cultura: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
 

    async def delete_cultura(self, id: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DELETE_CULTURA, (id,))
                self.connection.commit()
                
                if cursor.rowcount == 0:
                    return error_response(
                        message=CULTURA_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                return success_response(
                    message=CULTURA_DELETED_MSG
                )
                
        except Exception as e:
            logger.error("Error en delete_cultura: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
