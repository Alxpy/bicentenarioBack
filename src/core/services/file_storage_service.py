from src.presentation.dto.file_dto import FileDTO, ResponseFileDTO
from src.core.abstractions.services.file_storage_service_abstract import IFileStorageService
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.repository.connection_file_storage import GCSClient

class FileStorageService:
    
    def __init__(self):
        self.cliente = GCSClient()
  
    async def upload_file(self, data_file: FileDTO) -> Response:
        try:
            file = self.cliente.upload_file(data_file.file, data_file.file_name)
            return success_response(
                message="File uploaded successfully",
                data=ResponseFileDTO(
                    file_url=file,
                ),
            )
        except Exception as e:
            return error_response(
                message=(f'File upload failed ${str(e)}'),
            )