from src.core.abstractions.infrastructure.repository.ubicacion_repository_abstract import IUbicacionRepository
from src.core.abstractions.services.ubicacion_service_abstract import IUbicacionService
from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.dto.ubicacion_dto import UbicacionDTO

class UbicacionService(IUbicacionService):
    
    def __init__(self, ubicacion_repository: IUbicacionRepository):
        self.ubicacion_repository = ubicacion_repository
    
    async def get_all_ubicaciones(self) -> list[UbicacionDomain]:
        return await self.ubicacion_repository.get_all_ubicaciones()
    
    async def get_ubicacion_by_id(self, id: int) -> UbicacionDomain:
        return await self.ubicacion_repository.get_ubicacion_by_id(id)
    
    async def get_ubicacion_by_name(self, nombre: str) -> UbicacionDomain:
        return await self.ubicacion_repository.get_ubicacion_by_name(nombre)
    
    async def create_ubicacion(self, ubicacion: UbicacionDTO) -> None:
        return await self.ubicacion_repository.create_ubicacion(ubicacion)
    
    async def update_ubicacion(self, id: int, ubicacion: UbicacionDomain) -> None:
        return await self.ubicacion_repository.update_ubicacion(id, ubicacion)
    
    async def delete_ubicacion(self, id: int) -> None:
        return await self.ubicacion_repository.delete_ubicacion(id)