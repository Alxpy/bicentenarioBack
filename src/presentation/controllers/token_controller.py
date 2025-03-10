from fastapi import APIRouter, Depends, HTTPException, Query, status
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
