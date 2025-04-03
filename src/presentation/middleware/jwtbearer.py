from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

class JWTBearer(HTTPBearer):
    def __init__(self, required_roles: list[str] = None, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.required_roles = required_roles or []

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, 
                    detail="Esquema de autenticación inválido"
                )
            
            token = credentials.credentials
            secret_key = os.getenv("JWT_SECRET")
            
            try:
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                
                if self.required_roles:
                    user_roles = payload.get("roles", [])
                    if not any(role in user_roles for role in self.required_roles):
                        raise HTTPException(
                            status_code=403,
                            detail="No tienes permisos para acceder a este recurso"
                        )
                
                request.state.user = payload
                return payload
                
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=403, detail="Token expirado")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=403, detail="Token inválido")
        else:
            raise HTTPException(status_code=403, detail="Token de autorización faltante")