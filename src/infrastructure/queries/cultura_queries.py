GET_ALL_CULTARAS = """
    SELECT c.id, c.nombre, c.imagen, c.descripcion,c.id_ubicacion, ct.nombre as nombre_ubicacion
    FROM cultura AS c
    INNER JOIN ubicacion AS ct ON c.id_ubicacion = ct.id
"""

GET_CULTURA_BY_ID = """
    SELECT c.id, c.nombre, c.imagen, c.descripcion,c.id_ubicacion, ct.nombre as nombre_ubicacion
    FROM cultura AS c
    INNER JOIN ubicacion AS ct ON c.id_ubicacion = ct.id
    WHERE c.id = %s
"""

GET_CULTURA_BY_NOMBRE= """
    SELECT c.id, c.nombre, c.imagen, c.descripcion,c.id_ubicacion, ct.nombre as nombre_ubicacion
    FROM cultura AS c 
    INNER JOIN ubicacion AS ct ON c.id_ubicacion = ct.id
    WHERE c.nombre = %s    
"""

GET_CULTURA_BY_UBICACION = """
    SELECT c.id, c.nombre, c.imagen, c.descripcion, c.id_ubicacion, ct.nombre AS nombre_ubicacion
    FROM cultura c
    INNER JOIN ubicacion AS ct ON c.id_ubicacion = ct.id
    WHERE ct.nombre = %s;

"""

CREATE_CULTURA = """
    INSERT INTO cultura (nombre, imagen, descripcion, id_ubicacion) VALUES (%s, %s, %s, %s)
"""

UPDATE_CULTURA = """
    UPDATE cultura 
    SET nombre = %s, imagen = %s, descripcion = %s, id_ubicacion = %s
    WHERE id = %s    
"""
DELETE_CULTURA = """DELETE FROM cultura WHERE id = %s"""