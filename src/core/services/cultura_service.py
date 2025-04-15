from src.core.abstractions.infrastructure.repository.cultura_repository_abstract import ICulturaRepository
from src.core.abstractions.services.cultura_service_abstract import ICulturaService
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO

class CulturaService(ICulturaService):

    def __init__(self, cultura_repository: ICulturaRepository):
        self.cultura_repository = cultura_repository
    
    async def get_all_culturas(self) -> list[CulturaDomain]:
        return await self.cultura_repository.get_all_culturas()
    
    async def get_cultura_by_id(self, id: int) -> CulturaDomain:
        return await self.cultura_repository.get_cultura_by_id(id)
    
    async def get_cultura_by_nombre(self, nombre: str) -> CulturaDomain:
        return await self.cultura_repository.get_cultura_by_nombre(nombre)
    
    async def get_cultura_by_ubicacion(self, ubicacion: str) -> CulturaDomain:
        return await self.cultura_repository.get_cultura_by_ubicacion(ubicacion)

    async def create_cultura(self, cultura: CulturaDTO) -> None:
        return await self.cultura_repository.create_cultura(cultura)
    
    async def update_cultura(self, id: int, cultura: CulturaDomain) -> None:
        return await self.cultura_repository.update_cultura(id, cultura)
    
    async def delete_cultura(self, id: int) -> None:
        return await self.cultura_repository.delete_cultura(id)