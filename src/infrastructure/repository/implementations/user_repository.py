import bcrypt
import mysql.connector
from mysql.connector import pooling
from typing import Optional

from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.user_queries import *

class UserRepository(IUsuarioRepository):
    def __init__(self, connection_pool) -> None:
        self.connection_pool = connection_pool

    def _get_connection(self):
        """Obtiene una conexión del pool"""
        return self.connection_pool

    async def get_usuario(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_USER_BY_ID, (id,))
                result = cursor.fetchone()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND, 
                        success=False, 
                        message=USER_NOT_FOUND_MSG
                    )
                
                # Convertir roles a lista
                result['roles'] = result['roles'].split(',') if result['roles'] else []
                
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message="Usuario encontrado.",
                    data=UsuarioDomain(**result)
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()

    async def get_all_usuarios(self) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(GET_ALL_USERS)
                result = cursor.fetchall()
                
                if not result:
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=NO_USERS_MSG
                    )
                
                # Convertir roles a lista para cada usuario
                for usuario in result:
                    usuario['roles'] = usuario['roles'].split(',') if usuario['roles'] else []
                
                usuarios = [UsuarioDomain(**usuario) for usuario in result]
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=USERS_FOUND_MSG,
                    data=usuarios
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()

    async def create_usuario(self, usuario: UsuarioDTO) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            conn.start_transaction()
            
            hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
            
            with conn.cursor() as cursor:
                # Insertar usuario
                cursor.execute(CREATE_USER, (
                    usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno,
                    usuario.correo, hashed_password, usuario.genero,
                    usuario.telefono, usuario.pais, usuario.ciudad
                ))
                
                # Asignar rol por defecto
                cursor.execute(ASSIGN_DEFAULT_ROLE)
                
                conn.commit()
                return Response(
                    status=HTTP_201_CREATED,
                    success=True,
                    message=USER_CREATED_MSG
                )
                
        except mysql.connector.IntegrityError as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_400_BAD_REQUEST,
                success=False,
                message=EMAIL_EXISTS_MSG if "Duplicate entry" in str(e) else str(e)
            )
        except Exception as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()

    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            conn.start_transaction()
            
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_USER, (
                    usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno,
                    usuario.correo, usuario.genero, usuario.telefono,
                    usuario.pais, usuario.ciudad, id
                ))
                
                if cursor.rowcount == 0:
                    conn.rollback()
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=USER_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=USER_UPDATED_MSG
                )
                
        except mysql.connector.IntegrityError as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_400_BAD_REQUEST,
                success=False,
                message=f"Error de integridad: {str(e)}"
            )
        except Exception as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()

    async def change_password(self, id: int, password: str) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            conn.start_transaction()
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_PASSWORD, (hashed_password, id))
                
                if cursor.rowcount == 0:
                    conn.rollback()
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=USER_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=PASSWORD_UPDATED_MSG
                )
                
        except Exception as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()

    async def delete_usuario(self, id: int) -> Response:
        conn = None
        try:
            conn = self._get_connection()
            conn.start_transaction()
            
            with conn.cursor() as cursor:
                cursor.execute(DELETE_USER, (id,))
                
                if cursor.rowcount == 0:
                    conn.rollback()
                    return Response(
                        status=HTTP_404_NOT_FOUND,
                        success=False,
                        message=USER_NOT_FOUND_MSG
                    )
                
                conn.commit()
                return Response(
                    status=HTTP_200_OK,
                    success=True,
                    message=USER_DELETED_MSG
                )
                
        except Exception as e:
            if conn:
                conn.rollback()
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if conn:
                conn.close()