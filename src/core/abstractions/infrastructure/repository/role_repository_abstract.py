from abc import abstractmethod, ABC
from src.core.models.rol_domain import RolDomain
from src.presentation.responses.response_factory import Response
class IRolRepository(ABC) :
    
    @abstractmethod
    async def get_all_roles(self) -> Response:
        """Get all roles."""
        pass