from src.core.models.multimedia_domain import MultimediaDomain
from src.presentation.dto.multimedia_dto import MultimediaDTO

def map_multimedia_domain_to_dto(multimedia: MultimediaDomain) -> MultimediaDTO:
    return MultimediaDTO(
        id=0,
        enlace=multimedia.enlace,
        tipo=multimedia.tipo,
    )