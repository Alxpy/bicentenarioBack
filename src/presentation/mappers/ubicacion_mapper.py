from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.dto.ubicacion_dto import UbicacionDTO

def map_ubicacion_domain_to_dto(ubicacion: UbicacionDomain) -> UbicacionDTO:
    return UbicacionDTO(
        id=0,
        nombre=ubicacion.nombre,
        latitud=ubicacion.latitud,
        longitud=ubicacion.longitud,
        descripcion=ubicacion.descripcion,
        imagen=ubicacion.imagen
    )