from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.biblioteca_service_abstract import IBibliotecaService
from src.core.dependency_injection.dependency_injection import build_biblioteca_service
from src.presentation.dto.biblioteca_dto import BibliotecaDTO, BibliotecaUpdateDTO
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.responses.base_response import Response

biblioteca_router = APIRouter(prefix="/api/v1/library", tags=["library"])

# ─────────────────────────────────────────────
# 📌 Create a new library entry
# ─────────────────────────────────────────────
@biblioteca_router.post(
    "",
    response_model=Response[None],
    summary="Create new library entry"
)
async def create_biblioteca(
    biblioteca: BibliotecaDTO,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.create_biblioteca(biblioteca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 📚 Get all library entries
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "",
    response_model=Response[list[BibliotecaDomain]],
    summary="List all library entries"
)
async def get_bibliotecas(
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_all_bibliotecas()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🔍 Get library entry by ID
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "/{id}",
    response_model=Response[BibliotecaDomain],
    summary="Get library entry by ID"
)
async def get_biblioteca_by_id(
    id: int,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_biblioteca_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🔍 Get library entries by category
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "/ByCategory/{categoryName}",
    response_model=Response[list[BibliotecaDomain]],
    summary="Filter by category"
)
async def get_bibliotecas_by_category(
    categoryName: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_biblioteca_by_category(categoryName)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🔍 Get library entry by title
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "/ByTitle/{title}",
    response_model=Response[BibliotecaDomain],
    summary="Search by title"
)
async def get_biblioteca_by_title(
    title: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_biblioteca_by_title(title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🔍 Get library entries by author
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "/ByAuthor/{author}",
    response_model=Response[list[BibliotecaDomain]],
    summary="Filter by author"
)
async def get_bibliotecas_by_author(
    author: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_biblioteca_by_author(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🔍 Get library entries by publication date
# ─────────────────────────────────────────────
@biblioteca_router.get(
    "/ByPublicationDate/{publicationDate}",
    response_model=Response[list[BibliotecaDomain]],
    summary="Filter by publication date"
)
async def get_bibliotecas_by_publication_date(
    publicationDate: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.get_biblioteca_by_publication_date(publicationDate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# ✏️ Update library entry by ID
# ─────────────────────────────────────────────
@biblioteca_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update library entry"
)
async def update_biblioteca(
    id: int,
    biblioteca_update: BibliotecaUpdateDTO,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        existing = await biblioteca_service.get_biblioteca_by_id(id)

        updated = BibliotecaDomain(
            id=id,
            titulo=biblioteca_update.titulo,
            autor=biblioteca_update.autor,
            imagen=biblioteca_update.imagen,
            fecha_publicacion=biblioteca_update.fecha_publicacion,
            edicion=biblioteca_update.edicion,
            id_tipo=biblioteca_update.id_tipo,
            id_usuario=existing.id_usuario,
            fuente=biblioteca_update.fuente,
            enlace=biblioteca_update.enlace,
        )
        return await biblioteca_service.update_biblioteca(id, updated)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────────
# 🗑️ Delete library entry by ID
# ─────────────────────────────────────────────
@biblioteca_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete library entry"
)
async def delete_biblioteca(
    id: int,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await biblioteca_service.delete_biblioteca(id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
