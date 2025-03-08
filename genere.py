import os

class OnionArchitecture:

    def __init__(self, name: str, dir_project: str):
        self.name = name
        self.dir_project = os.path.join(os.getcwd(), dir_project)

    def create_folders(self):

        try:
            core_dirs = [
                "src/core/abstractions/services",
                "src/core/abstractions/infrastructure/repository",
                "src/core/models",
                "src/core/services",
                "src/core/dependency_injection"
            ]
            
            infrastructure_dirs = [
                "src/infrastructure/repository/dependency_injection",
                "src/infrastructure/repository/implementations"
            ]
            
            presentation_dirs = [
                "src/presentation/controllers",
                "src/presentation/dto",
                "src/presentation/mappers"
            ]
            
            all_dirs = core_dirs + infrastructure_dirs + presentation_dirs
            
            for directory in all_dirs:
                os.makedirs(os.path.join(self.dir_project, directory), exist_ok=True)
            
            return "Estructura de carpetas creada exitosamente."
        except Exception as e:
            return f"Error al crear carpetas: {e}"

    def create_property_files(self):
        try:
            files = [
                "src/core/dependency_injection/dependency_injection.py",
                "src/infrastructure/repository/dependency_injection/dependency_injection.py",
                "src/infrastructure/repository/connection.py"
            ]
            
            for file in files:
                file_path = os.path.join(self.dir_project, file)
                with open(file_path, "w") as f:
                    # Código para dependency_injection.py y connection.py
                    if "connection.py" in file:
                        f.write("""from mysql.connector import pooling, Error
import os

# Configuración de la conexión a la base de datos MySQL
connection_pool = pooling.MySQLConnectionPool(
    pool_name=os.getenv("DB_POOL_NAME"),
    pool_size=int(os.getenv("DB_POOL_SIZE")),
    pool_reset_session=True,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    connection_timeout=int(os.getenv("DB_TIMEOUT")),
    charset=os.getenv("DB_CHARSET"),
    collation=os.getenv("DB_COLLATION")
)

# Función para obtener una conexión desde el pool
def get_connection():
    try:
        connection = connection_pool.get_connection()

        if not connection.is_connected():
            connection.reconnect(attempts=3, delay=2)

        return connection
    except Error as e:
        print(f"Error al obtener conexión del pool: {e}")
        return None
    """)
                    else:
                        if "src/infrastructure/repository/dependency_injection" in file:
                            f.write("""
from src.infrastructure.repository.connection import get_connection


def get_db_connection():
    connection = get_connection()
    try:
        yield connection
    finally:
        if connection is not None:
            connection.close()

                                    """)
                        else:
                            f.write("""
from fastapi import Depends
from src.infrastructure.repository.connection import get_connection        
                    """)
            
            return "Archivos de configuración creados exitosamente."
        except Exception as e:
            return f"Error al crear archivos: {e}"


    def create_files(self, name_file: str):

        try:
            name_upper = name_file.capitalize()
            files = {
                f"src/core/abstractions/infrastructure/repository/{name_file}_repository_abstract.py": f"""
from abc import ABC, abstractmethod
from src.core.models.{name_file}_domain import {name_upper}Domain

class I{name_upper}Repository(ABC):

    @abstractmethod
    async def method_example(self):
        pass
""",
                f"src/core/abstractions/services/{name_file}_service_abstract.py": f"""
from abc import ABC, abstractmethod
from src.core.models.{name_file}_domain import {name_upper}Domain

class I{name_upper}Service(ABC):

    @abstractmethod
    async def method_example(self):
        pass
""",
                f"src/core/services/{name_file}_service.py": f"""from src.core.abstractions.infrastructure.repository.{name_file}_repository_abstract import I{name_upper}Repository
from src.core.abstractions.services.{name_file}_service_abstract import I{name_upper}Service
from src.core.models.{name_file}_domain import {name_upper}Domain


class {name_upper}Service(I{name_upper}Service):

    def __init__(self, {name_file}Repository: I{name_upper}Repository):
        self.{name_file}Repository = {name_file}Repository
        
    async def method_example(self):
        return await self.{name_file}Repository.method_example()
        
""",
                f"src/core/models/{name_file}_domain.py": f"""
from pydantic import BaseModel
from typing import Optional

class {name_upper}Domain(BaseModel):

    
                """,
                f"src/infrastructure/repository/implementations/{name_file}_repository.py": f"""
from src.core.abstractions.infrastructure.repository.{name_file}_repository_abstract import I{name_upper}Repository
from src.core.models.{name_file}_domain import {name_upper}Domain

class {name_upper}Repository(I{name_upper}Repository):

    def __init__(self, connection):
        self.connection = connection
        
    async def method_example(self):
        pass
        
""",
                f"src/presentation/controllers/{name_file}_controller.py": f"""
from fastapi import APIRouter, HTTPException, Depends, Query
from src.core.abstractions.services.{name_file}_service_abstract import I{name_upper}Service
from src.core.dependency_injection.dependency_injection import build_{name_file}_service
from src.presentation.dto.{name_file}_dto import {name_upper}Dto
from src.presentation.mappers.{name_file}_mapper import {name_upper}Mapper
from src.core.models.{name_file}_domain import {name_upper}Domain


{name_file}_controller = APIRouter(prefix="/api/v1", tags=["{name_file}"])

@{name_file}_controller.get("/")
async def method_example(
    service: I{name_upper}Service = Depends(build_{name_file}_service),
):
    try:
        return await service.method_example()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
""",
                f"src/presentation/dto/{name_file}_dto.py": "# DTO\n",
                f"src/presentation/mappers/{name_file}_mapper.py": "# Mapper\n"
            }
            
            for file, content in files.items():
                file_path = os.path.join(self.dir_project, file)
                with open(file_path, "w") as f:
                    f.write(content)
            
            return "Archivos del módulo creados exitosamente."
        except Exception as e:
            return f"Error al crear archivos: {e}"

    def add_dependency_injection(self, name_file: str):
        try:
            dependency_injection_file = "src/core/dependency_injection/dependency_injection.py"
            full_path = os.path.join(self.dir_project, dependency_injection_file)

            import_statement = f"from src.core.services.{name_file}_service import {name_file.capitalize()}Service\n" \
                            f"from src.infrastructure.repository.implementations.{name_file}_repository import {name_file.capitalize()}Repository\n"

            function_definition = f"\ndef build_{name_file}_service(db_connection=Depends(get_connection)):\n" \
                                f"    return {name_file.capitalize()}Service({name_file.capitalize()}Repository(db_connection))\n"

            with open(full_path, "r+") as f:
                content = f.read()

                if import_statement not in content:
                    f.seek(0, 0) 
                    f.write(import_statement + content)

                if f"def build_{name_file}_service" not in content:
                    f.write(function_definition)

            return f"Dependencia y función de servicio para {name_file} agregados correctamente."

        except Exception as e:
            return f"Error al agregar la dependencia o función: {e}"



    def add_method(self, method_name: str, action: str, name_file: str):
        try:
            files = [
                f"src/core/abstractions/infrastructure/repository/{name_file}_repository_abstract.py",
                f"src/core/abstractions/services/{name_file}_service_abstract.py",
                f"src/core/services/{name_file}_service.py",
                f"src/infrastructure/repository/implementations/{name_file}_repository.py"
            ]
            
            if action in ["get", "create", "update", "delete"]:
                method_content = self.generate_controller_method(name_file, name_file.capitalize(), action, method_name)
            else:
                method_content = "    pass"
            
            method_definition = f"\ndef {method_name}(self):\n{method_content}\n"

            for file in files:
                full_path = os.path.join(self.dir_project, file)
                if not os.path.exists(full_path):
                    return f"El archivo {file} no existe."
                
                with open(full_path, "a") as f:
                    f.write(method_definition)

            controller_file = f"src/presentation/controllers/{name_file}_controller.py"
            controller_path = os.path.join(self.dir_project, controller_file)
            if os.path.exists(controller_path):
                method_content_controller = self.generate_controller_method(name_file, name_file.capitalize(), action, method_name)
                with open(controller_path, "a") as f:
                    f.write(method_content_controller)
            
            return f"Método {method_name} agregado correctamente a los archivos."

        except Exception as e:
            return f"Error al agregar el método: {e}"

    def generate_controller_method(self, name_file: str, name_upper: str, action: str, method_name: str):
        """
        Método para generar el contenido del método en el controller según la acción.
        """
        if action == "get":
            return f"""
@{name_file}_controller.get("/{method_name}")
async def {name_file}_get(
    service: I{name_upper}Service = Depends(build_{name_file}_service),
):
    try:
        return await service.{name_file}_get()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        """
        
        elif action == "create":
            return f"""
@{name_file}_controller.post("/{method_name}")
async def {name_file}_create(
    {name_file}_data: {name_upper}CreateDTO,
    service: I{name_upper}Service = Depends(build_{name_file}_service),
):
    try:
        return await service.create_{name_file}({name_file}_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        """
        
        elif action == "update":
            return f"""
@{name_file}_controller.put("/{method_name}/{{id}}")
async def {name_file}_update(
    id: int,
    {name_file}_data: {name_upper}UpdateDTO,
    service: I{name_upper}Service = Depends(build_{name_file}_service),
):
    try:
        return await service.update_{name_file}(id, {name_file}_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        """
        
        elif action == "delete":
            return f"""
@{name_file}_controller.delete("/{method_name}/{{id}}")
async def {name_file}_delete(
    id: int,
    service: I{name_upper}Service = Depends(build_{name_file}_service),
):
    try:
        await service.delete_{name_file}(id)
        return {{"message": "{name_file} deleted successfully"}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        """
        
        else:
            return "    pass"



if __name__ == "__main__":
    project = OnionArchitecture("Tarea1", "D:/Alex/I 2025 Uni/281/proyecto/presentaciones/Tarea1/")
    print(project.create_folders())
    print(project.create_property_files())
    #print(project.create_files("user"))
    #print(project.add_dependency_injection("user"))
    #print(project.add_method("get_ap",   "get",        "user"      ))
