from src.core.models.historia_domain import HistoriaDomain
from src.presentation.dto.historia_dto import HistoriaDTO

def map_historia_domain_to_dto(historia: HistoriaDomain) -> HistoriaDTO:
    return HistoriaDTO(
        id=0,
        titulo=historia.titulo,
        descripcion=historia.descripcion,
        fecha_inicio=historia.fecha_inicio,
        fecha_fin=historia.fecha_fin,
        imagen=historia.imagen,
        id_ubicacion=historia.id_ubicacion,
        id_categoria=historia.id_categoria,      
    )