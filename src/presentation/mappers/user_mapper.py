from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO

def map_usuario_domain_to_dto(usuarioDTO: UsuarioDTO) -> UsuarioDTO:
    return UsuarioDTO(
        id=0,
        nombre=usuarioDTO.nombre,
        apellidoPaterno=usuarioDTO.apellidoPaterno,
        apellidoMaterno=usuarioDTO.apellidoMaterno,
        correo=usuarioDTO.correo,
        contrasena=usuarioDTO.contrasena,
        genero=usuarioDTO.genero,
        telefono=usuarioDTO.telefono,
        pais=usuarioDTO.pais,
        ciudad=usuarioDTO.ciudad,
        estado=0,
        id_rol=2
    )
