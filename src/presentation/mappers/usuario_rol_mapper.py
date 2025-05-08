from src.core.models.usuario_rol_domain import UsuarioRolDomain
from src.presentation.dto.usuario_rol_dto import UsuarioRolDTO

def map_usuario_rol_domain_to_dto(usuario_rol: UsuarioRolDomain) -> UsuarioRolDTO: 
    return UsuarioRolDTO(
        id_usuario=usuario_rol.id_usuario,
        id_rol=usuario_rol.id_rol
    )