from src.core.abstractions.infrastructure.repository.evento_repository_abstract import IEventoRepository
from src.core.abstractions.services.evento_service_abstract import IEventoService
from src.core.models.evento_domain import EventoDomain
from src.presentation.dto.evento_dto import EventoDTO, EventoPostDTO, EventoUpdateDTO
from src.resources.responses.response import Response

class EventoService(IEventoService):
    
    def __init__(self, evento_repository: IEventoRepository):
        self.evento_repository = evento_repository
    
    async def get_all_eventos(self) -> Response:
        return await self.evento_repository.get_all_eventos()
    
    async def get_evento_by_id(self, id: int) -> Response:
        return await self.evento_repository.get_evento_by_id(id)
    
    async def get_evento_by_nombre(self, nombre: str) -> Response:
        return await self.evento_repository.get_evento_by_nombre(nombre)
    
    async def get_evento_by_fecha(self, fecha: str) -> Response:
        return await self.evento_repository.get_evento_by_fecha(fecha)
    
    async def get_evento_by_tipo(self, tipo: str) -> Response:
        return await self.evento_repository.get_evento_by_tipo(tipo)
    
    async def get_evento_by_ubicacion(self, ubicacion: str) -> Response:
        return await self.evento_repository.get_evento_by_ubicacion(ubicacion)

    async def create_evento(self, evento: EventoPostDTO) -> Response:
        return await self.evento_repository.create_evento(evento)
    
    async def update_evento(self, id: int, evento: EventoUpdateDTO) -> Response:
        return await self.evento_repository.update_evento(id, evento)
    
    async def delete_evento(self, id: int) -> Response:
        return await self.evento_repository.delete_evento(id)
    