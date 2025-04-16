from src.core.abstractions.infrastructure.repository.multimedia_cultura_repository_abstract import IMultimediaCulturaRepository
from src.core.abstractions.services.multimedia_cultura_service_abstract import IMultimediaCulturaService
from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain
from src.presentation.dto.multimedia_cultura_dto import MultimediaCulturaDTO
from src.resources.responses.response import Response 

class MultimediaCulturaService(IMultimediaCulturaService):
    def __init__(self, multimedia_cultura_repository: IMultimediaCulturaRepository):
        self.multimedia_cultura_repository = multimedia_cultura_repository
    
    async def get_all_multimedia_cultura(self) -> Response:
        return await self.multimedia_cultura_repository.get_all_multimedia_cultura()
    
    async def get_multimedia_cultura_by_id_cultura(self, id: int) -> Response:
        return await self.multimedia_cultura_repository.get_multimedia_cultura_by_id_cultura(id)
    
    async def create_multimedia_cultura(self, multimedia_cultura: MultimediaCulturaDTO) -> None:
        return await self.multimedia_cultura_repository.create_multimedia_cultura(multimedia_cultura)
    
    async def delete_multimedia_cultura(self, id: int) -> None:
        return await self.multimedia_cultura_repository.delete_multimedia_cultura(id)