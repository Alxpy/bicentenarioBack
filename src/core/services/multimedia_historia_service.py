from src.core.abstractions.infrastructure.repository.multimedia_historia_respository_abstract import IMultimediaHistoriaRepository
from src.core.abstractions.services.multimedia_historia_service_abstract import IMultimediaHistoriaService
from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain
from src.presentation.dto.multimedia_historia_dto import MultimediaHistoriaDTO


class MultimediaHistoriaService(IMultimediaHistoriaService):

    def __init__(self, multimedia_historia_repository: IMultimediaHistoriaRepository):
        self.multimedia_historia_repository = multimedia_historia_repository

    async def get_all_multimedia_historia(self) -> list[MultimediaHistoriaDomain]:
        return await self.multimedia_historia_repository.get_all_multimedia_historia()
    
    async def get_multimedia_historia_by_id(self, id: int) -> list[MultimediaHistoriaDomain]:
        return await self.multimedia_historia_repository.get_multimedia_historia_by_id(id)

    async def create_multimedia_historia(self, multimedia_historia: MultimediaHistoriaDTO) -> None:
        return await self.multimedia_historia_repository.create_multimedia_historia(multimedia_historia)
    
    async def delete_multimedia_historia(self, id: int) -> None:
        return await self.multimedia_historia_repository.delete_multimedia_historia(id)
    