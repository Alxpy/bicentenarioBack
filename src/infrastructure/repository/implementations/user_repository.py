import bcrypt
import mysql.connector
from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO

class UserRepository(IUsuarioRepository):
    def __init__(self, connection: object) -> None:
        self.connection = connection

    async def get_usuario(self, id: int):
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                               SELECT 
                                    u.id, 
                                    u.nombre, 
                                    u.correo, 
                                    u.contrasena, 
                                    u.cantIntentos, 
                                    u.estado, 
                                    u.email_verified_at, 
                                    u.ultimoIntentoFallido, 
                                    GROUP_CONCAT(ur.id_rol) AS roles
                                FROM usuario AS u
                                INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                                WHERE u.id = %s
                                GROUP BY u.id;
                               """, (id,))
                result = cursor.fetchone()
                if result:
                    return {"success": True, "usuario": UsuarioDomain(**result)}
                return {"success": False, "message": "Usuario no encontrado."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}

    async def get_all_usuarios(self):
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                               SELECT 
                                u.id, 
                                u.nombre, 
                                u.correo, 
                                u.contrasena, 
                                u.cantIntentos, 
                                u.estado, 
                                u.email_verified_at, 
                                u.ultimoIntentoFallido, 
                                GROUP_CONCAT(ur.id_rol) AS roles
                            FROM usuario AS u
                            INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                            GROUP BY u.id;
                """)
                result = cursor.fetchall()
                if result:
                    return {"success": True, "usuarios": [UsuarioDomain(**usuario) for usuario in result]}
                return {"success": False, "message": "No hay usuarios registrados."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}

    async def create_usuario(self, usuario: UsuarioDTO):
        try:
            with self.connection.cursor() as cursor:
                hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    """
                    INSERT INTO usuario (nombre, apellidoPaterno, apellidoMaterno, correo, contrasena, genero, telefono, pais, ciudad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno, usuario.correo, hashed_password,
                     usuario.genero, usuario.telefono, usuario.pais, usuario.ciudad)
                )
                self.connection.commit()
                return {"success": True, "message": "Usuario Creado"}
        except mysql.connector.IntegrityError:
            return {"success": False, "message": "El correo electrónico ya está registrado."}
        except Exception:
            return {"success": False, "message": "Error."}

    async def update_usuario(self, id: int, usuario: UsuarioDomain):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuario 
                    SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, correo = %s, contrasena = %s, 
                        genero = %s, telefono = %s, pais = %s, ciudad = %s, estado = %s, id_rol = %s
                    WHERE id = %s
                    """,
                    (usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno, usuario.correo, usuario.contrasena,
                     usuario.genero, usuario.telefono, usuario.pais, usuario.ciudad, usuario.estado, usuario.id_rol, id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Usuario no encontrado."}
                self.connection.commit()
                return {"success": True, "message": "Usuario actualizado correctamente."}
        except mysql.connector.IntegrityError:
            return {"success": False, "message": "Error de integridad en la actualización."}
        except Exception as err:
            print(f"Error: {err}")
            return {"success": False, "message": "Error."}

    async def delete_usuario(self, id: int):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
                if cursor.rowcount == 0:
                    return {"success": False, "message": "Usuario no encontrado."}
                self.connection.commit()
                return {"success": True, "message": "Usuario eliminado correctamente."}
        except Exception:
            return {"success": False, "message": "Error ."}
