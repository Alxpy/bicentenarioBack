from abc import abstractmethod, ABC
from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.dto.ubicacion_dto import UbicacionDTO

class IUbicacionRepository(ABC):

    @abstractmethod
    async def get_ubicacion_by_id(self, id: int) -> UbicacionDomain:
        pass
    
    @abstractmethod
    async def get_all_ubicaciones(self) -> list[UbicacionDomain]:
        pass

    @abstractmethod
    async def get_ubicacion_by_name(self, nombre: str) -> UbicacionDomain:
        pass
    
    @abstractmethod
    async def create_ubicacion(self, ubicacion: UbicacionDTO) -> None:
        pass
    
    @abstractmethod
    async def update_ubicacion(self, id: int, ubicacion: UbicacionDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_ubicacion(self, id: int) -> None:
        pass