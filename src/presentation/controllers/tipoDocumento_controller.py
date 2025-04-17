from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.tipoDocumento_service_abstract import ITipoDocumentoService
from src.core.dependency_injection.dependency_injection import build_tipoDocumento_service
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.responses.response_factory import Response

document_type_router = APIRouter(
    prefix="/api/v1/documentTypes",
    tags=["Document Types"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Document type not found"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request data"}
    }
)

@document_type_router.post(
    "",
    response_model=Response[TipoDocumentoDomain],
    status_code=status.HTTP_201_CREATED,
    summary="Create document type",
    description="Creates a new document type classification in the system."
)
async def create_document_type(
    document_type: TipoDocumentoDTO,
    service: ITipoDocumentoService = Depends(build_tipoDocumento_service)
):
    try:
        return await service.create_tipo_documento(document_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create document type: {str(e)}"
        )

@document_type_router.get(
    "",
    response_model=Response[list[TipoDocumentoDomain]],
    summary="List all document types",
    description="Retrieves all available document type classifications."
)
async def get_all_document_types(
    service: ITipoDocumentoService = Depends(build_tipoDocumento_service)
):
    try:
        return await service.get_all_tipos_documento()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve document types: {str(e)}"
        )

@document_type_router.get(
    "/{id}",
    response_model=Response[TipoDocumentoDomain],
    summary="Get document type by ID",
    description="Retrieves details of a specific document type by its unique identifier."
)
async def get_document_type_by_id(
    id: int,
    service: ITipoDocumentoService = Depends(build_tipoDocumento_service)
):
    try:
        result = await service.get_tipo_documento(id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document type with ID {id} not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@document_type_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update document type",
    description="Modifies an existing document type classification."
)
async def update_document_type(
    id: int,
    document_type_update: TipoDocumentoDTO,
    service: ITipoDocumentoService = Depends(build_tipoDocumento_service)
):
    try:
        updated_type = TipoDocumentoDomain(tipo=document_type_update.tipo)
        return await service.update_tipo_documento(id, updated_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update document type: {str(e)}"
        )

@document_type_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete document type",
    description="Removes a document type classification from the system."
)
async def delete_document_type(
    id: int,
    service: ITipoDocumentoService = Depends(build_tipoDocumento_service)
):
    try:
        return await service.delete_tipo_documento(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete document type: {str(e)}"
        )