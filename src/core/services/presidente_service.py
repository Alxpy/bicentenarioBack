from src.core.abstractions.infrastructure.repository.presidente_repository_abstract import IPresidenteRepository
from src.core.abstractions.services.presidente_service_abstract import IPresidenteService
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.dto.presidente_dto import PresidenteDTO

class PresidenteService(IPresidenteService):
    
    def __init__(self, presidente_repository: IPresidenteRepository):
        self.presidente_repository = presidente_repository
    
    async def get_all_presidentes(self) -> list[PresidenteDomain]:
        return await self.presidente_repository.get_all_presidentes()
    
    async def get_presidente_by_id(self, id: int) -> PresidenteDomain:
        return await self.presidente_repository.get_presidente_by_id(id)
    
    async def get_presidente_by_nombre(self, nombre: str) -> PresidenteDomain:
        return await self.presidente_repository.get_presidente_by_nombre(nombre)
    
    async def create_presidente(self, presidente: PresidenteDTO) -> None:
        return await self.presidente_repository.create_presidente(presidente)
    
    async def update_presidente(self, id: int, presidente: PresidenteDomain) -> None:
        return await self.presidente_repository.update_presidente(id, presidente)
    
    async def delete_presidente(self, id: int) -> None:
        return await self.presidente_repository.delete_presidente(id)