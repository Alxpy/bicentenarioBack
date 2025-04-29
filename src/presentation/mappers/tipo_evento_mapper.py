from src.core.models.tipo_evento_domain import TipoEventoDomain
from src.presentation.dto.tipo_evento_dto import TipoEventoDTO

def map_tipo_evento_domain_to_dto(tipo_evento: TipoEventoDomain) -> TipoEventoDTO:
    return TipoEventoDTO(
        id=tipo_evento.id,
        nombre_evento=tipo_evento.nombre_evento,
    )
