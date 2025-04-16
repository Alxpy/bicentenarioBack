import bcrypt
import mysql.connector
import logging
from mysql.connector import IntegrityError
from typing import List, Optional

from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO, NewPasswordDTO
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.user_queries import *
from src.infrastructure.queries.auth_queries import VERIFY_EMAIL

logger = logging.getLogger(__name__)

class UserRepository(IUsuarioRepository):
    def __init__(self, connection) -> None:
        self.connection = connection


    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[List[dict]]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")

    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización y retorna el rowcount"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing update: {str(e)}")

    async def get_usuario(self, id: int) -> Response:
        """Obtiene un usuario por su ID"""
        try:
            result = await self._execute_query(GET_USER_BY_ID, (id,))
            
            if not result:
                logger.info(f"Usuario no encontrado con ID: {id}")
                return error_response(
                    message=USER_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            # Convertir roles a lista
            result['roles'] = result['roles'].split(',') if result['roles'] else []
            logger.info(f"Usuario encontrado ID: {id}")
            
            return success_response(
                data=UsuarioDomain(**result),
                message=USER_FOUND_MSG
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_all_usuarios(self) -> Response:
        """Obtiene todos los usuarios registrados"""
        try:
            result = await self._execute_query(GET_ALL_USERS, fetch_all=True)
            
            if not result:
                logger.info("No se encontraron usuarios")
                return error_response(
                    message=NO_USERS_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            # Convertir roles a lista para cada usuario
            for usuario in result:
                usuario['roles'] = usuario['roles'].split(',') if usuario['roles'] else []
            
            logger.info(f"Encontrados {len(result)} usuarios")
            return success_response(
                data=[UsuarioDomain(**usuario) for usuario in result],
                message=USERS_FOUND_MSG
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_usuario(self, usuario: UsuarioDTO) -> Response:
        """Crea un nuevo usuario"""
        try:
            hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
            
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # Insertar usuario
                cursor.execute(CREATE_USER, (
                    usuario.nombre, 
                    usuario.apellidoPaterno, 
                    usuario.apellidoMaterno,
                    usuario.correo, 
                    hashed_password, 
                    usuario.genero,
                    usuario.telefono, 
                    usuario.pais, 
                    usuario.ciudad
                ))
                
                # Asignar rol por defecto
                cursor.execute(ASSIGN_DEFAULT_ROLE)
                conn.commit()
                
                logger.info(f"Usuario creado con email: {usuario.correo}")
                return success_response(
                    message=USER_CREATED_MSG,
                    status=HTTP_201_CREATED
                )
                
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear usuario: {str(e)}")
            return error_response(
                message=EMAIL_EXISTS_MSG if "Duplicate entry" in str(e) else str(e),
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creando usuario: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> Response:
        """Actualiza un usuario existente"""
        try:
            rowcount = await self._execute_update(UPDATE_USER, (
                usuario.nombre, 
                usuario.apellidoPaterno, 
                usuario.apellidoMaterno,
                usuario.correo, 
                usuario.genero, 
                usuario.telefono,
                usuario.pais, 
                usuario.ciudad, 
                id
            ))
            
            if rowcount == 0:
                logger.info(f"Intento de actualizar usuario no existente ID: {id}")
                return error_response(
                    message=USER_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Usuario actualizado ID: {id}")
            return success_response(
                message=USER_UPDATED_MSG
            )
            
        except IntegrityError as e:
            logger.error(f"Error de integridad al actualizar usuario ID {id}: {str(e)}")
            return error_response(
                message=f"Error de integridad: {str(e)}",
                status=HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error actualizando usuario ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def change_password(self, data: NewPasswordDTO) -> Response:
        """Cambia la contraseña de un usuario"""
        try:
            hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
            
            conn = self._get_connection()
            with conn.cursor() as cursor:
                # Verificar código de verificación
                cursor.execute(VERIFY_EMAIL, (data.correo, data.code))
                user = cursor.fetchone()
                
                if not user:
                    logger.info(f"Código inválido para usuario: {data.correo}")
                    return error_response(
                        message=INVALID_CODE_MSG,
                        status=HTTP_400_BAD_REQUEST
                    )
                
                # Actualizar contraseña
                rowcount = await self._execute_update(
                    UPDATE_PASSWORD, 
                    (hashed_password, data.correo)
                )
                
                if rowcount == 0:
                    logger.info(f"Usuario no encontrado al cambiar contraseña: {data.correo}")
                    return error_response(
                        message=USER_NOT_FOUND_MSG,
                        status=HTTP_404_NOT_FOUND
                    )
                
                logger.info(f"Contraseña actualizada para usuario: {data.correo}")
                return success_response(
                    message=PASSWORD_UPDATED_MSG
                )
                
        except Exception as e:
            logger.error(f"Error cambiando contraseña: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def delete_usuario(self, id: int) -> Response:
        """Elimina un usuario"""
        try:
            rowcount = await self._execute_update(DELETE_USER, (id,))
            
            if rowcount == 0:
                logger.info(f"Intento de eliminar usuario no existente ID: {id}")
                return error_response(
                    message=USER_NOT_FOUND_MSG,
                    status=HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Usuario eliminado ID: {id}")
            return success_response(
                message=USER_DELETED_MSG
            )
            
        except Exception as e:
            logger.error(f"Error eliminando usuario ID {id}: {str(e)}")
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )