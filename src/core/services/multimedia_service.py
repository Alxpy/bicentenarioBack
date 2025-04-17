from src.core.abstractions.infrastructure.repository.multimedia_repository_abstract import IMultimediaRepository
from src.core.abstractions.services.multimedia_service_abstract import IMultimediaService
from src.core.models.multimedia_domain import MultimediaDomain
from src.presentation.dto.multimedia_dto import MultimediaDTO

class MultimediaService(IMultimediaService):

    def __init__(self, multimedia_repository: IMultimediaRepository):
        self.multimedia_repository = multimedia_repository

    async def get_all_multimedia(self) -> list[MultimediaDomain]:
        return await self.multimedia_repository.get_all_multimedia()
    
    async def get_multimedia_by_id(self, id: int) -> MultimediaDomain:
        return await self.multimedia_repository.get_multimedia_by_id(id)
    
    async def create_multimedia(self, multimedia: MultimediaDTO) -> None:
        return await self.multimedia_repository.create_multimedia(multimedia)
    
    async def update_multimedia(self, id: int, multimedia: MultimediaDomain) -> None:
        return await self.multimedia_repository.update_multimedia(id, multimedia)
    
    async def delete_multimedia(self, id: int) -> None:
        return await self.multimedia_repository.delete_multimedia(id)
    