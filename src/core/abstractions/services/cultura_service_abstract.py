from abc import ABC, abstractmethod
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO

class ICulturaService(ABC):
    @abstractmethod
    async def get_all_culturas(self) -> list[CulturaDomain]:
        pass

    @abstractmethod
    async def get_cultura_by_id(self, id: int) -> CulturaDomain:
        pass

    @abstractmethod
    async def get_cultura_by_nombre(self, nombre: str) -> CulturaDomain:
        pass

    @abstractmethod
    async def get_cultura_by_ubicacion(self, ubicacion:str) -> list[CulturaDomain]:
        pass
    
    @abstractmethod
    async def create_cultura(self, cultura: CulturaDTO) -> None:
        pass

    @abstractmethod
    async def update_cultura(self, id: int, cultura: CulturaDomain) -> None:
        pass

    @abstractmethod
    async def delete_cultura(self, id: int) -> None:
        pass