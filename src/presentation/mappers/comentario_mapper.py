from src.core.models.comentario_domain import ComentarioDomain
from src.presentation.dto.comentario_dto import ComentarioDTO, ComentarioUpdateDTO

def map_comentario_domain_to_dto(comentario: ComentarioDomain) -> ComentarioDTO:
    return ComentarioDTO(
        id=0,
        id_usuario=comentario.id_usuario,
        contenido=comentario.contenido,
        fecha_creacion=comentario.fecha_creacion,
    )