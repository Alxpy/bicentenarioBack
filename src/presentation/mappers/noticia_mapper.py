from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.dto.noticia_dto import NoticiaDTO

def map_noticia_domain_to_dto(noticia: NoticiaDomain) -> NoticiaDTO:
    return NoticiaDTO(
        id=0,
        titulo=noticia.titulo,
        resumen=noticia.resumen,
        contenido=noticia.contenido,
        imagen=noticia.imagen,
        id_Categoria=noticia.id_Categoria,
        id_usuario=noticia.id_usuario,
        fecha_publicacion=noticia.fecha_publicacion 
    )