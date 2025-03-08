import bcrypt
from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.models.user_domain import UsuarioDomain

class UserRepository(IUsuarioRepository):
    
    def __init__(self, connection:object)->object:
        self.connection = connection

    
    
    async def get_usuario(self, id: int) -> UsuarioDomain:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (id,))
                result = cursor.fetchone()
                return UsuarioDomain(**result)            
        except Exception as e:
            print({"Error": e})
            return None
    
    
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        list_usuarios = []
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario")
                result = cursor.fetchall()
                for usuario in result:
                    list_usuarios.append(UsuarioDomain(**usuario))
                return list_usuarios
        except Exception as e:
            print({"Error": e})
            return None
    
    async def create_usuario(self, usuario: UsuarioDomain) -> int:
        try:
            with self.connection.cursor() as cursor:
                hashed_password = bcrypt.hashpw(usuario.contrasena.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    """
                    INSERT INTO usuario (nombre, apellidoPaterno,apellidoMaterno,correo, contrasena, genero, telefono, pais, ciudad, estado,id_rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno, usuario.correo, hashed_password , usuario.genero, usuario.telefono, usuario.pais, usuario.ciudad, usuario.estado, usuario.id_rol)
                )
                self.connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print({"Error": e})
            return None
    
    
    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> None:
        try:
          
            with self.connection.cursor() as cursor:               
                cursor.execute(
                    """
                    UPDATE usuario SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, correo = %s, contrasena = %s, genero = %s, telefono = %s, pais = %s, ciudad = %s, estado = %s, id_rol = %s
                    WHERE id = %s
                    """,
                    (usuario.nombre, usuario.apellidoPaterno, usuario.apellidoMaterno, usuario.correo, usuario.contrasena, usuario.genero, usuario.telefono, usuario.pais, usuario.ciudad, usuario.estado, usuario.id_rol, id)
                )
                self.connection.commit()
        except Exception as e:
            print({"Error": e})
            return None
    
    
    async def delete_usuario(self, id: int) -> None:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
                self.connection.commit()
        except Exception as e:
            print({"Error": e})
            return None
        
    
    