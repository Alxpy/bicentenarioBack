from src.core.models.evento_domain import EventoDomain
from src.presentation.dto.evento_dto import EventoDTO, EventoPostDTO, EventoUpdateDTO

def map_evento_domain_to_dto(evento: EventoDomain) -> EventoDTO:
    return EventoDTO(
        id=evento.id,
        nombre=evento.nombre,
        descripcion=evento.descripcion,
        imagen=evento.imagen,
        fecha_inicio=evento.fecha_inicio,
        fecha_fin=evento.fecha_fin,
        id_tipo_evento=evento.id_tipo_evento,
        id_ubicacion=evento.id_ubicacion,
        id_usuario=evento.id_usuario
    )