from src.core.abstractions.infrastructure.repository.usuario_evento_repository_abstract import IUsuarioEventoRepository
from src.core.abstractions.services.usuario_evento_service_abstract import IUsuarioEventoService
from src.core.models.usuario_evento_domain import UsuarioEventoDomain
from src.presentation.dto.usuario_evento_dto import UsuarioEventoDTO, UpdateAsistioUsuarioEventoDTO
from src.resources.responses.response import Response

class UsuarioEventoService(IUsuarioEventoService):
    def __init__(self, usuario_evento_repository: IUsuarioEventoRepository):
        self.usuario_evento_repository = usuario_evento_repository

    async def get_usuario_evento_by_id_usuario(self, id: int) -> Response:
        return await self.usuario_evento_repository.get_usuario_evento_by_id_usuario(id)

    async def get_usuario_evento_by_id_evento(self, id:int) -> Response:
        return await self.usuario_evento_repository.get_usuario_evento_by_id_evento(id)

    async def get_all_usuario_eventos(self) -> Response:
        return await self.usuario_evento_repository.get_all_usuario_eventos()

    async def create_usuario_evento(self, usuario_evento: UsuarioEventoDTO) -> None:
        return await self.usuario_evento_repository.create_usuario_evento(usuario_evento)

    async def update_asistio_usuario_evento(self, id: int, asistio: UpdateAsistioUsuarioEventoDTO) -> None:
        return await self.usuario_evento_repository.update_asistio_usuario_evento(id, asistio)

    async def delete_usuario_evento(self, id: int) -> None:
        return await self.usuario_evento_repository.delete_usuario_evento(id)
    
    async def get_data_usuario_evento(self) -> Response:
        return await self.usuario_evento_repository.get_data_usuario_evento()
    