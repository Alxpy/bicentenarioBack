from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.biblioteca_service_abstract import IBibliotecaService
from src.core.dependency_injection.dependency_injection import build_biblioteca_service
from src.presentation.dto.biblioteca_dto import BibliotecaDTO, BibliotecaUpdateDTO
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.responses.base_response import Response

biblioteca_controller = APIRouter(prefix="/api/v1", tags=["biblioteca"])

# ─────────────────────────────────────────────
# 📌 Create a new biblioteca
# ─────────────────────────────────────────────
@biblioteca_controller.post("/biblioteca", response_model=Response[None])
async def createBiblioteca(
    biblioteca: BibliotecaDTO,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.create_biblioteca(biblioteca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 📚 Get all bibliotecas
# ─────────────────────────────────────────────
@biblioteca_controller.get("/bibliotecas", response_model=Response[list[BibliotecaDomain]])
async def getBibliotecas(
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_all_bibliotecas()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🔍 Get biblioteca by ID
# ─────────────────────────────────────────────
@biblioteca_controller.get("/biblioteca/{id}", response_model=Response[BibliotecaDomain])
async def getBibliotecaById(
    id: int,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_biblioteca_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🔍 Get biblioteca by category, title, author or date
# ─────────────────────────────────────────────
@biblioteca_controller.get("/biblioteca/category/{categoryName}", response_model=Response[list[BibliotecaDomain]])
async def getBibliotecaByCategory(
    categoryName: str,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_biblioteca_by_category(categoryName)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@biblioteca_controller.get("/biblioteca/title/{title}", response_model=Response[BibliotecaDomain])
async def getBibliotecaByTitle(
    title: str,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_biblioteca_by_title(title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@biblioteca_controller.get("/biblioteca/author/{author}", response_model=Response[list[BibliotecaDomain]])
async def getBibliotecaByAuthor(
    author: str,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_biblioteca_by_author(author)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@biblioteca_controller.get("/biblioteca/publicationDate/{publicationDate}", response_model=Response[list[BibliotecaDomain]])
async def getBibliotecaByPublicationDate(
    publicationDate: str,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.get_biblioteca_by_publication_date(publicationDate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# ✏️ Update biblioteca by ID
# ─────────────────────────────────────────────
@biblioteca_controller.put("/biblioteca/{id}", response_model=Response[None])
async def updateBiblioteca(
    id: int,
    bibliotecaUpdate: BibliotecaUpdateDTO,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        existingBiblioteca: BibliotecaDomain = await bibliotecaService.get_biblioteca_by_id(id)

        updatedBiblioteca = BibliotecaDomain(
            id=id,
            titulo=bibliotecaUpdate.titulo,
            autor=bibliotecaUpdate.autor,
            imagen=bibliotecaUpdate.imagen,
            fecha_publicacion=bibliotecaUpdate.fecha_publicacion,
            edicion=bibliotecaUpdate.edicion,
            id_tipo=bibliotecaUpdate.id_tipo,
            id_usuario=existingBiblioteca.id_usuario,
            fuente=bibliotecaUpdate.fuente,
            enlace=bibliotecaUpdate.enlace,
        )
        return await bibliotecaService.update_biblioteca(id, updatedBiblioteca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🗑️ Delete biblioteca by ID
# ─────────────────────────────────────────────
@biblioteca_controller.delete("/biblioteca/{id}", response_model=Response[None])
async def deleteBiblioteca(
    id: int,
    bibliotecaService: IBibliotecaService = Depends(build_biblioteca_service)
):
    try:
        return await bibliotecaService.delete_biblioteca(id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
