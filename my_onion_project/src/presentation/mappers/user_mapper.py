from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO

def map_usuario_domain_to_dto(usuarioDTO: UsuarioDTO) -> UsuarioDTO:
    return UsuarioDTO(
        id=usuarioDTO.id,
        nombre=usuarioDTO.nombre,
        apellidoPaterno=usuarioDTO.apellidoPaterno,
        apellidoMaterno=usuarioDTO.apellidoMaterno,
        correo=usuarioDTO.correo,
        contrasena=usuarioDTO.contrasena,
        genero=usuarioDTO.genero,
        telefono=usuarioDTO.telefono,
        pais=usuarioDTO.pais,
        ciudad=usuarioDTO.ciudad,
        estado=usuarioDTO.estado,
        id_rol=usuarioDTO.id_rol
    )
