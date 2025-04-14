from src.core.abstractions.services.role_service_abstract import IRolSerice
from src.core.abstractions.infrastructure.repository.role_repository_abstract import IRolRepository
from src.core.models.rol_domain import RolDomain

class RolRepository(IRolSerice):
    
    def __init__(self, rol_repository: IRolRepository):
        self.rol_repository = rol_repository
        
    async def get_all_roles(self) -> list[RolDomain]:
        return self.rol_repository.get_all_roles()
    