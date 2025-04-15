from abc import ABC, abstractmethod
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.dto.presidente_dto import PresidenteDTO

class IPresidenteService(ABC):
        
    @abstractmethod
    async def get_all_presidentes(self) -> list[PresidenteDomain]:
        pass

    @abstractmethod
    async def get_presidente_by_id(self, id: int) -> PresidenteDomain:
        pass
    
    @abstractmethod
    async def get_presidente_by_nombre(self, nombre: str) -> PresidenteDomain:
        pass
    
    @abstractmethod
    async def create_presidente(self, presidente: PresidenteDTO) -> None:
        pass
    
    @abstractmethod
    async def update_presidente(self, id: int, presidente: PresidenteDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_presidente(self, id: int) -> None:
        pass