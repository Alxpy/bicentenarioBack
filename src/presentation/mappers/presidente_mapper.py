from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.dto.presidente_dto import PresidenteDTO

def map_presidente_domain_to_dto(presidente: PresidenteDomain) -> PresidenteDTO:
    return PresidenteDTO(
        id=0,
        id_usuario=presidente.id_usuario,
        nombre=presidente.nombre,
        apellido=presidente.apellido,
        imagen=presidente.imagen,
        inicio_periodo=presidente.inicio_periodo,
        fin_periodo=presidente.fin_periodo,
        bibliografia=presidente.bibliografia,
        partido_politico=presidente.partido_politico,
        principales_politicas=presidente.principales_politicas
    )