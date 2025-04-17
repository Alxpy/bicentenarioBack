from pydantic import BaseModel
from fastapi import UploadFile

class FileDTO(BaseModel):
    file: str
    file_name: str

class UploadFileDTO(BaseModel):
    file_name: UploadFile
    temp_path: str
    
class ResponseFileDTO(BaseModel):
    file_url: str