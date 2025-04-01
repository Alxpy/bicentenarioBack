from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.tipoDocumento_service_abstract import ITipoDocumentoService
from src.core.dependency_injection.dependency_injection import build_tipoDocumento_service
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO
from src.presentation.mappers.tipoDocumento_mapper import map_tipoDocumento_domain_to_dto
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain

tipoDocumento_controller = APIRouter(prefix="/api/v1", tags=["tipoDocumento"])

@tipoDocumento_controller.post("/tipoDocumento")
async def create_tipoDocumento(
    tipoDocumento: TipoDocumentoDTO,
    tipoDocumento_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await tipoDocumento_service.create_tipo_documento(tipoDocumento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipoDocumento_controller.get("/tipoDocumentos")
async def get_tipoDocumentos(
    tipoDocumento_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await tipoDocumento_service.get_all_tipos_documento()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipoDocumento_controller.get("/tipoDocumento/{id}")
async def get_tipoDocumento(
    id: int,
    tipoDocumento_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await tipoDocumento_service.get_tipo_documento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipoDocumento_controller.put("/tipoDocumento/{id}")
async def update_tipoDocumento(
    id: int,
    tipoDocumentoUpdate: TipoDocumentoDTO,
    tipoDocumento_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        updateTipoDocumento = TipoDocumentoDomain(
            tipo=tipoDocumentoUpdate.tipo,
        )
        return await tipoDocumento_service.update_tipo_documento(id, updateTipoDocumento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipoDocumento_controller.delete("/tipoDocumento/{id}")
async def delete_tipoDocumento(
    id: int,
    tipoDocumento_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await tipoDocumento_service.delete_tipo_documento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))