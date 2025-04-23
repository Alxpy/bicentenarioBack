from fastapi import Depends, APIRouter, HTTPException, Query
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *

routes_controller = APIRouter(prefix="/api/v1/routes", tags=["routes"])
from src.presentation.middleware.jwtbearer import JWTBearer

@routes_controller.get("/admin", dependencies=[Depends(JWTBearer(["admin"]))])
async def admin_dashboard():
    return Response(
        status= HTTP_200_OK, 
        success=True,
        message="Bienvenido al dashboard de administrador"
    )

@routes_controller.get("/user", dependencies=[Depends(JWTBearer(["user"]))])
async def user_profile():
    return Response(
        status= HTTP_200_OK, 
        success=True,
        message="Bienvenido al perfil de usuario"
    )