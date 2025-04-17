from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.tipoDocumento_service_abstract import ITipoDocumentoService
from src.core.dependency_injection.dependency_injection import build_tipoDocumento_service
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.responses.response_factory import Response

document_type_controller = APIRouter(prefix="/api/v1/documentType", tags=["documentType"])

@document_type_controller.post("", response_model=Response[TipoDocumentoDomain])
async def create_document_type(
    document_type: TipoDocumentoDTO,
    document_type_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await document_type_service.create_tipo_documento(document_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@document_type_controller.get("/getAll", response_model=Response[list[TipoDocumentoDomain]])
async def get_all_document_types(
    document_type_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await document_type_service.get_all_tipos_documento()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@document_type_controller.get("/getById/{id}", response_model=Response[TipoDocumentoDomain])
async def get_document_type_by_id(
    id: int,
    document_type_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await document_type_service.get_tipo_documento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@document_type_controller.put("/{id}", response_model=Response[None])
async def update_document_type(
    id: int,
    document_type_update: TipoDocumentoDTO,
    document_type_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        updated_document_type = TipoDocumentoDomain(
            tipo=document_type_update.tipo,
        )
        return await document_type_service.update_tipo_documento(id, updated_document_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@document_type_controller.delete("/{id}", response_model=Response[None])
async def delete_document_type(
    id: int,
    document_type_service: ITipoDocumentoService = Depends(build_tipoDocumento_service)):
    try:
        return await document_type_service.delete_tipo_documento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
