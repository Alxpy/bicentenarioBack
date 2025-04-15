GET_ALL_UBICACIONES = """
SELECT u.id,u.nombre,u.latitud,u.longitud,u.imagen,u.descripcion
FROM ubicacion u
"""

GET_UBICACION_BY_ID = """
SELECT u.id,u.nombre,u.latitud,u.longitud,u.imagen,u.descripcion
FROM ubicacion u
WHERE u.id = %s
"""

GET_UBICACION_BY_NAME = """
    SELECT u.id,u.nombre,u.latitud,u.longitud,u.imagen,u.descripcion
    FROM ubicacion u
    WHERE u.nombre = %s
"""

CREATE_UBICACION = """
    INSERT INTO ubicacion (nombre, latitud, longitud, imagen, descripcion)
    VALUES (%s, %s, %s, %s, %s)
""" 

UPDATE_UBICACION = """
    UPDATE ubicacion
    SET nombre = %s, latitud = %s, longitud = %s, imagen = %s, descripcion = %s
    WHERE id = %s

"""

DELETE_UBICACION = """
    DELETE FROM ubicacion WHERE id = %s
"""
