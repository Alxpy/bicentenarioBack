from src.presentation.responses.base_response import Response
from pydantic import BaseModel
from src.infrastructure.constants.http_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST

def success_response(data=None, message="", status=HTTP_200_OK):
    return Response(status=status, success=True, message=message, data=data)

def error_response(message, status=HTTP_400_BAD_REQUEST):
    return Response(status=status, success=False, message=message, data=None)
