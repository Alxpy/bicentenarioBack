import bycrypt
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
                if result:
                    return UsuarioDomain(
                        id=result["id"],
                        nombre=result["nombre"],
                        apellidoPaterno=result["apellidoPaterno"],
                        apellidoMaterno=result["apellidoMaterno"],
                        correo=result["correo"],
                        contrasena=result["contrasena"],
                        genero=result["genero"],
                        telefono=result["telefono"],
                        pais=result["pais"],
                        ciudad=result["ciudad"],
                        estado=result["estado"],                        
                        id_rol=result["id_rol"]
                    )
        except Exception as error:
            print(f"Error al obtener usuario: {str(error)}")
        return None
    
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        lista_usuarios = []
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario")
                result = cursor.fetchall()
                print(result)
                for row in result:
                    usuario=UsuarioDomain(
                        id=row["id"],
                        nombre=row["nombre"],
                        apellidoPaterno=row["apellidoPaterno"],
                        apellidoMaterno=row["apellidoMaterno"],
                        correo=row["correo"],
                        contrasena=row["contrasena"],
                        genero=row["genero"],
                        telefono=row["telefono"],
                        pais=row["pais"],
                        ciudad=row["ciudad"],
                        estado=row["estado"],
                        id_rol=row["id_rol"]                        
                    )
                    lista_usuarios.append(usuario)
                return lista_usuarios
        except Exception as error:
            print(f"Error al obtener usuarios: {str(error)}")
            return []


    
    async def get_by_correo(self, correo:str)->UsuarioDomain:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
                result = cursor.fetchone()
                if result:
                    return UsuarioDomain(
                        id=result["id"],
                        nombre=result["nombre"],
                        apellidoPaterno=result["apellidoPaterno"],
                        apellidoMaterno=result["apellidoMaterno"],
                        correo=result["correo"],
                        contrasena=result["contrasena"],
                        genero=result["genero"],
                        telefono=result["telefono"],
                        pais=result["pais"],
                        ciudad=result["ciudad"],
                        id_rol=result["id_rol"]
                    )
        except Exception as error:
            print(f"Error al obtener usuario por correo: {str(error)}")
        return None
    
    async def create_usuario(self, usuario: UsuarioDomain) -> int:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuario (nombre, apellidoPaterno, apellidoMaterno, correo, contrasena, genero, telefono, pais, ciudad, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        usuario.nombre,
                        usuario.apellidoPaterno,
                        usuario.apellidoMaterno,
                        usuario.correo,
                        usuario.contrasena,
                        usuario.genero,
                        usuario.telefono,
                        usuario.pais,
                        usuario.ciudad,
                        usuario.id_rol
                    )
                )
                self.connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_id = cursor.fetchone()[0]
                return cursor.lastrowid
        except Exception as err:
            print(f"Error al crear usuario: {err}")
        return None
        

    async def update_usuario(self, id: int, usuario: UsuarioDomain):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuario SET
                    nombre = %s,apellidoPaterno = %s, apellidoMaterno = %s,
                    correo = %s,contrasena = %s,genero = %s,
                    telefono = %s, pais = %s,ciudad = %s,
                    estado = %s, id_rol = %s
                    WHERE id = %s
                    """,
                    (
                        usuario.nombre,
                        usuario.apellidoPaterno,
                        usuario.apellidoMaterno,
                        usuario.correo,
                        usuario.contrasena,
                        usuario.genero,
                        usuario.telefono,
                        usuario.pais,
                        usuario.ciudad,
                        usuario.estado,
                        usuario.id_rol,
                        id
                    )
                )
                self.connection.commit()
                return True
        except Exception as err:
            print(f"Error al actualizar usuario: {err}")
            return False
    
    async def delete_usuario(self, id: int) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
                self.connection.commit()
                return True
        except Exception as err:
            print(f"Error al eliminar usuario: {err}")
            return False
    
    async def delete_by_correo(self, correo: str) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM usuario WHERE correo = %s", (correo,))
                self.connection.commit()
                return True
        except Exception as err:
            print(f"Error al eliminar usuario por correo: {err}")
            return False
    
    async def registrar_usuario(self, usuario: UsuarioDomain):
        try:
            with self.connection.cursor() as cursor:
                hashed_password = bycrypt.hashpw(usuario.contrasena.encode("utf-8"), bycrypt.gensalt())
                cursor.execute(
                    "INSERT INTO usuario (nombre, apellidoPaterno, apellidoMaterno, correo, contrasena, genero, telefono, pais, ciudad, estado, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        usuario.nombre,
                        usuario.apellidoPaterno,
                        usuario.apellidoMaterno,
                        usuario.correo,
                        hashed_password,
                        usuario.genero,
                        usuario.telefono,
                        usuario.pais,
                        usuario.ciudad,
                        usuario.estado,
                        usuario.id_rol
                    )
                )
                self.connection.commit()
                return True
        except Exception as err:
            print(f"Error al registrar usuario: {err}")
            return False

    async def login_usuario(self, correo: str, contrasenaLg: str) -> UsuarioDomain:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                print(cursor)
                cursor.execute("""SELECT nombre, apelliPaterno, apellidoMaterno, correo, genero, telefono, pais, ciudad, estado,
                                FROM usuario WHERE correo = %s
                               """, (correo,))
                user_row=cursor.fetchone()
                if not user_row:
                    return None
                if not user_row ["estado"]:
                    return None
                if not bycrypt.checkpw(contrasenaLg.encode("utf-8"), user_row["contrasena"].encode("utf-8")):
                    return None
                
                return UsuarioDomain(
                    nombre=user_row["nombre"],
                    apellidoPaterno=user_row["apellidoPaterno"],
                    apellidoMaterno=user_row["apellidoMaterno"],
                    correo=user_row["correo"],
                    genero=user_row["genero"],
                    telefono=user_row["telefono"],
                    pais=user_row["pais"],
                    ciudad=user_row["ciudad"],
                    estado=user_row["estado"]
                )
        except Exception as err:
            print(f"Error al iniciar sesión: {err}")
            return None