from src.core.models.usuario_evento_domain import UsuarioEventoDomain
from src.presentation.dto.usuario_evento_dto import UsuarioEventoDTO, UpdateAsistioUsuarioEventoDTO

def map_usuario_evento_domain_to_dto(usuario_evento: UsuarioEventoDomain) -> UsuarioEventoDTO:
    return UsuarioEventoDTO(
        id=usuario_evento.id,
        id_usuario=usuario_evento.id_usuario,
        id_evento=usuario_evento.id_evento,
        asistio=usuario_evento.asistio
    )