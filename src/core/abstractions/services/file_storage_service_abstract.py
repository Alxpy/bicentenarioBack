from abc  import ABC, abstractmethod
from src.presentation.dto.file_dto import FileDTO

class IFileStorageService(ABC):
    
    @abstractmethod
    async def upload_file(self, data_file: FileDTO) -> str:
        """
        Uploads a file to the storage service and returns the URL of the uploaded file.
        """
        pass