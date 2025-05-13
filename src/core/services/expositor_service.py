from src.core.models.expositor_domain import ExpositorDomain
from src.presentation.dto.expositor_dto import ExpositorCreate
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.repository.implementations.expositor_repository import ExpositorRepository

class ExpositorService:
    def __init__(self, expositor_repository: ExpositorRepository) -> None:
        self.expositor_repository = expositor_repository

    async def get_all_expositores(self) -> Response:
        return await self.expositor_repository.get_all()

    async def create_expositor(self, expositor: ExpositorCreate) -> Response:
        return await self.expositor_repository.create(expositor)
    
    async def create_expositor_evento(self,id_evento, id_expositor) -> Response:
        return await self.expositor_repository.create_expositor_evento(id_evento, id_expositor)
    
    async def get_all_expositores_by_evento(self, id_evento: int) -> Response:
        return await self.expositor_repository.get_all_expositores_by_evento(id_evento)
    
    async def delete_expositor_evento(self, id_evento: int, id_expositor: int) -> Response:
        return await self.expositor_repository.delete_expositor_evento(id_evento, id_expositor)