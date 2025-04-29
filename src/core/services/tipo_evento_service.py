from src.core.abstractions.infrastructure.repository.tipo_evento_repository_abstract import ITipoEventoRepository
from src.core.abstractions.services.tipo_evento_abstract import ITipoEventoService
from src.core.models.tipo_evento_domain import TipoEventoDomain
from src.presentation.dto.tipo_evento_dto import TipoEventoDTO
from src.resources.responses.response import Response


class TipoEventoService(ITipoEventoService):
    def __init__(self, tipo_evento_repository: ITipoEventoRepository):
        self.tipo_evento_repository = tipo_evento_repository

    async def get_tipo_evento_by_id(self, id: int) -> Response:
        return await self.tipo_evento_repository.get_tipo_evento_by_id(id)

    async def get_all_tipo_eventos(self) -> Response:
        return await self.tipo_evento_repository.get_all_tipo_eventos()

    async def create_tipo_evento(self, tipo_evento: TipoEventoDTO) -> None:
        return await self.tipo_evento_repository.create_tipo_evento(tipo_evento)

    async def update_tipo_evento(self, id: int, tipo_evento: TipoEventoDomain) -> None:
        return await self.tipo_evento_repository.update_tipo_evento(id, tipo_evento)

    async def delete_tipo_evento(self, id: int) -> None:
        return await self.tipo_evento_repository.delete_tipo_evento(id)
