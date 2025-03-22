import bcrypt
import jwt
import mysql.connector
from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO
from src.resources.responses.response import Response

class UserRepository(IUsuarioRepository):
    def __init__(self, connection: object) -> None:
        self.connection = connection

    async def get_usuario(self, id: int) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, u.contrasena, u.genero, u.telefono, 
                    u.pais, u.ciudad, u.estado, u.email_verified_at, u.ultimoIntentoFallido, u.codeValidacion, u.cantIntentos, u.imagen, 
                    GROUP_CONCAT(r.nombre_rol) AS roles
                    FROM usuario AS u
                    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                    INNER JOIN rol AS r ON r.id = ur.id_rol
                    WHERE u.id = %s
                    GROUP BY u.id;
                """, (id,))
                result = cursor.fetchone()
                if result:
                    # Convertir el campo 'roles' de string a lista
                    roles = result['roles'].split(',') if result['roles'] else []
                    result['roles'] = roles  # Actualiza 'roles' con la lista
                    return Response(status=200, success=True, message="Usuario encontrado.", data=UsuarioDomain(**result))
                return Response(status=404, success=False, message="Usuario no encontrado.")
        except Exception as e:
            return Response(status=500, success=False, message=f"Error interno del servidor. Detalles: {str(e)}")


    async def get_all_usuarios(self) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, u.contrasena, u.cantIntentos, 
                        u.estado, u.email_verified_at, u.ultimoIntentoFallido, u.genero, u.telefono, u.pais, u.ciudad,
                        GROUP_CONCAT(r.nombre_rol) AS roles
                    FROM usuario AS u
                    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                    INNER JOIN rol AS r ON r.id = ur.id_rol
                    GROUP BY u.id;
                """)
                result = cursor.fetchall()
                if result:                    
                    for usuario in result:
                        roles = usuario['roles'].split(',') if usuario['roles'] else []
                        usuario['roles'] = roles 
                    
                    usuarios = [UsuarioDomain(**usuario) for usuario in result]
                    return Response(status=200, success=True, message="Usuarios encontrados.", data=usuarios)
                return Response(status=404, success=False, message="No hay usuarios registrados.")
        except Exception as e:
            return Response(status=500, success=False, message=f"Error interno del servidor. Detalles: {str(e)}")



    async def create_usuario(self, usuario: UsuarioDTO) -> Response:
        try:
            with self.connection.cursor() as cursor:
                hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("""
                    INSERT INTO usuario (nombre, apellidoPaterno, apellidoMaterno, correo, contrasena, genero, telefono, pais, ciudad)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno, usuario.correo, hashed_password,
                      usuario.genero, usuario.telefono, usuario.pais, usuario.ciudad))
                self.connection.commit()

            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuario_rol (id_usuario, id_rol)
                    SELECT u.id, r.id
                    FROM usuario u, rol r
                    WHERE u.correo = %s AND r.nombre_rol LIKE 'usuario'
                """, (usuario.correo,))
                self.connection.commit()
            return Response(status=201, success=True, message="Usuario creado correctamente.")
        except mysql.connector.IntegrityError:
            return Response(status=400, success=False, message="El correo electrónico ya está registrado.")
        except Exception:
            return Response(status=500, success=False, message="Error interno del servidor.")

    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> Response:
        try:
            update_values = [
                usuario.nombre,
                usuario.apellidoPaterno,
                usuario.apellidoMaterno,
                usuario.correo,
                usuario.genero,
                usuario.telefono,
                usuario.pais,
                usuario.ciudad
            ]
            
            if usuario.contrasena is not None:
                update_values.append(usuario.contrasena)
            else:
                update_values.append(None)
            
            set_clause = """
                SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, correo = %s, 
                    genero = %s, telefono = %s, pais = %s, ciudad = %s
            """
            
            if usuario.contrasena is not None:
                set_clause += ", contrasena = %s"

            with self.connection.cursor() as cursor:
                cursor.execute(f"""
                    UPDATE usuario 
                    {set_clause}
                    WHERE id = %s
                """, (*update_values, id))

                if cursor.rowcount == 0:
                    return Response(status=404, success=False, message="Usuario no encontrado.")
                
                self.connection.commit()
                return Response(status=200, success=True, message="Usuario actualizado correctamente.")
        
        except mysql.connector.IntegrityError as e:
            return Response(status=400, success=False, message=f"Error de integridad en la actualización: {str(e)}")
        
        except Exception as err:
            print(f"Error: {err}")
            return Response(status=500, success=False, message=f"Error interno del servidor. Detalles: {str(err)}")



    async def delete_usuario(self, id: int) -> Response:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE usuario SET estado = 3 WHERE id = %s", (id,))
                if cursor.rowcount == 0:
                    return Response(status=404, success=False, message="Usuario no encontrado.")
                self.connection.commit()
                return Response(status=200, success=True, message="Usuario eliminado correctamente.")
        except Exception:
            return Response(status=500, success=False, message="Error interno del servidor.")
