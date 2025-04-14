from src.core.abstractions.infrastructure.repository.role_repository_abstract import IRolRepository
from src.core.models.rol_domain import RolDomain
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import ROLES_NOT_FOUND_MSG, ROLES_FOUND_MSG
from src.infrastructure.queries.rol_queries import GET_ALL_ROLES
from src.resources.responses.response import Response

class RolRepository(IRolRepository):
    def __init__(self, conecction):
        self.conecction = conecction
        
    async def get_all_roles(self) -> Response:
        try:
            with self.conecction.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_ROLES)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=ROLES_NOT_FOUND_MSG
                    )
                    
                data = [RolDomain({**row}) for row in result]
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=ROLES_FOUND_MSG,
                    data=data
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"Internal server error. Details: {str(e)}"
            )