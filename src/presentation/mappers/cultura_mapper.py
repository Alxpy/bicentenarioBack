from src.core.models.cultura_domain import CulturaDomain
from src.presentation.dto.cultura_dto import CulturaDTO

def map_cultura_domain_to_dto(cultura: CulturaDomain) -> CulturaDTO:
    return CulturaDTO(
        id=0,
        nombre=cultura.nombre,
        imagen=cultura.imagen,
        descripcion=cultura.descripcion,
        id_ubicacion=cultura.id_ubicacion,        
    )