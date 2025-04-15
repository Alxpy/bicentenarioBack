from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.infrastructure.config.auth_config import JWT_ALGORITHM
from src.resources.responses.response import Response
from datetime import datetime
import jwt
import os

token_controller = APIRouter(prefix="/api/v1", tags=["token"])

@token_controller.get("/data")
async def get_data(token: str = Query(..., description="Token JWT recibido del front")):
    """
    Endpoint para obtener los datos almacenados en el token.
    """
    secret_key = os.getenv("JWT_SECRET")
    if not secret_key:
        raise HTTPException(status_code=500, detail="Secret key no configurada en el servidor.")

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return {"data": decoded_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error en la decodificación del token.")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")

@token_controller.get("/validate")
async def validate_token(
    token: str = Query(None, description="Token JWT recibido del front"),
    required_roles: list[str] = Query([], description="Roles requeridos para la ruta")
):
    """
    Endpoint para validar token y permisos de acceso
    """
    secret_key = os.getenv("JWT_SECRET")
    if not secret_key:
        raise HTTPException(status_code=500, detail="Secret key no configurada")

    try:
        clean_token = token.strip('"\' ') 
        
        payload = jwt.decode(clean_token, secret_key, algorithms=[JWT_ALGORITHM])
        
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            return {"valid": False, "message": "Token expirado"}
        
        user_roles = payload.get("roles", [])
        if required_roles and not any(role in user_roles for role in required_roles):
            return {
                "valid": False,
                "message": "Acceso no autorizado",
                "required_roles": required_roles,
                "user_roles": user_roles
            }
        
        return {
            "valid": True,
            "user": {
                "id": payload["id"],
                "nombre": payload["nombre"],
                "correo": payload["correo"],
                "roles": user_roles
            }
        }
        
    except jwt.ExpiredSignatureError:
        return {"valid": False, "message": "Token expirado"}
    except jwt.InvalidTokenError as e:
        return {"valid": False, "message": f"Token inválido: {str(e)}"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error validando token: {str(e)}"
        )