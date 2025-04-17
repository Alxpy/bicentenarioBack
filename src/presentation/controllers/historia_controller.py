from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.historia_service_abstract import IHistoriaService
from src.core.dependency_injection.dependency_injection import build_historia_service
from src.presentation.dto.historia_dto import HistoriaPostDTO, HistoriaUpdateDTO
from src.presentation.responses.base_response import Response
from src.core.models.historia_domain import HistoriaDomain

historia_router = APIRouter(
    prefix="/api/v1/history",
    tags=["History"]
)

# ─────────────────────────────────────────────
# 📌 Create a new history entry
# ─────────────────────────────────────────────
@historia_router.post(
    "",
    response_model=Response[None],
    summary="Create a new history entry",
    description="Adds a new historical record with its title, description, image, location, and associated category."
)
async def create_history(
    historia: HistoriaPostDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.create_historia(historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 📚 Get all history entries
# ─────────────────────────────────────────────
@historia_router.get(
    "",
    response_model=Response[list[HistoriaDomain]],
    summary="List all history entries",
    description="Retrieves a list of all historical records stored in the system."
)
async def get_histories(
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.get_all_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🔍 Get a specific history entry by ID
# ─────────────────────────────────────────────
@historia_router.get(
    "/{id}",
    response_model=Response[HistoriaDomain],
    summary="Get history by ID",
    description="Fetches a specific historical record using its unique identifier."
)
async def get_history_by_id(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.get_historia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🔍 Search history by title
# ─────────────────────────────────────────────
@historia_router.get(
    "/ByTitle/{title}",
    response_model=Response[HistoriaDomain],
    summary="Search history by title",
    description="Searches for a historical record by its title (case-sensitive match)."
)
async def get_history_by_title(
    title: str,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.get_historia_by_titulo(title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 📍 Filter history by location
# ─────────────────────────────────────────────
@historia_router.get(
    "/ByLocation/{location}",
    response_model=Response[list[HistoriaDomain]],
    summary="Filter history by location",
    description="Retrieves all historical records associated with a specific location."
)
async def get_history_by_location(
    location: str,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.get_historia_by_ubicacion(location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🗂️ Filter history by category
# ─────────────────────────────────────────────
@historia_router.get(
    "/ByCategory/{category}",
    response_model=Response[list[HistoriaDomain]],
    summary="Filter history by category",
    description="Retrieves all historical records classified under a specific category."
)
async def get_history_by_category(
    category: str,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.get_historia_by_categoria(category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# ✏️ Update a history entry by ID
# ─────────────────────────────────────────────
@historia_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update a history entry",
    description="Updates the data of a specific historical record using its ID. Partial updates are supported."
)
async def update_history(
    id: int,
    historia: HistoriaUpdateDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.update_historia(id, historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────
# 🗑️ Delete a history entry by ID
# ─────────────────────────────────────────────
@historia_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete a history entry",
    description="Removes a historical record from the database using its ID. This action is irreversible."
)
async def delete_history(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)
):
    try:
        return await historia_service.delete_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
