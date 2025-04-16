from src.core.abstractions.infrastructure.repository.role_repository_abstract import IRolRepository
from src.core.models.rol_domain import RolDomain
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.rol_queries import GET_ALL_ROLES
import logging
from typing import List


logger = logging.getLogger(__name__)

class RolRepository(IRolRepository):
    def __init__(self, connection):
        self.connection = connection
        
    async def get_all_roles(self) -> Response:
        """Obtiene todos los roles disponibles"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_ROLES)
                result = cursor.fetchall()
                
                if not result:
                    logger.info("No roles found in database")
                    return error_response(
                        message=ROLES_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                    
                roles = [RolDomain(**row) for row in result]
                logger.info(f"Found {len(roles)} roles")
                
                return success_response(
                    data=roles,
                    message=ROLES_FOUND_MSG
                )
                
        except Exception as e:
            logger.error(f"Error fetching roles: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )