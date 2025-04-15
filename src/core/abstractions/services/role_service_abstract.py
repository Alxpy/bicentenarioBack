from abc import abstractmethod, ABC
from src.core.models.rol_domain import RolDomain

class IRolSerice(ABC):
    
    @abstractmethod
    async def get_all_roles(self) -> list[RolDomain]:
        """Get all roles."""
        pass