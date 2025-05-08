from src.core.abstractions.infrastructure.repository.usuario_rol_repository_abstract import IUsuarioRolRepository
from src.core.abstractions.services.usuario_rol_service_abstract import IUsuarioRolService
from src.core.models.usuario_rol_domain import UsuarioRolDomain
from src.presentation.dto.usuario_rol_dto import UsuarioRolDTO
from src.resources.responses.response import Response


class UsuarioRolService(IUsuarioRolService):
    def __init__(self, usuario_rol_repository: IUsuarioRolRepository):
        self.usuario_rol_repository = usuario_rol_repository

    async def get_all_usuario_roles(self) -> Response:
        return await self.usuario_rol_repository.get_all_usuario_roles()

    async def get_usuario_rol_by_id_rol(self, id: int) -> Response:
        return await self.usuario_rol_repository.get_usuario_rol_by_id_rol(id)

    async def create_usuario_rol(self, usuario_rol: UsuarioRolDTO) -> None:
        return await self.usuario_rol_repository.create_usuario_rol(usuario_rol)

    async def delete_usuario_rol(self, id: int) -> None:
        return await self.usuario_rol_repository.delete_usuario_rol(id)
    