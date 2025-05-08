from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_evento_dto import ComentarioEventoDTO

def map_comentario_evento_domain_to_dto(comentario: ComentarioEventoDomain) -> ComentarioEventoDTO:
    return ComentarioEventoDTO(
        id_comentario=comentario.id_comentario,
        id_evento=comentario.id_evento
    )