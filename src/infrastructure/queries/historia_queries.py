GET_ALL_HISTORIA= """
    SELECT h.id, h.titulo, h.descripcion, h.fecha_inicio, h.fecha_fin, h.imagen, h.id_ubicacion, ct.nombre as nombre_ubicacion, id_categoria, c.nombre as nombre_categoria  
    FROM historia AS h
    INNER JOIN ubicacion AS ct ON h.id_ubicacion = ct.id
    INNER JOIN categoria_historia AS c ON h.id_categoria = c.id
"""

GET_HISTORIA_BY_ID = """
    SELECT h.id, h.titulo, h.descripcion, h.fecha_inicio, h.fecha_fin, h.imagen, h.id_ubicacion, ct.nombre as nombre_ubicacion, id_categoria, c.nombre as nombre_categoria
    FROM historia AS h
    INNER JOIN ubicacion AS ct ON h.id_ubicacion = ct.id
    INNER JOIN categoria_historia AS c ON h.id_categoria = c.id
    WHERE h.id = %s
"""

GET_HISTORIA_BY_TITULO = """
    SELECT h.id, h.titulo, h.descripcion, h.fecha_inicio, h.fecha_fin, h.imagen, h.id_ubicacion, ct.nombre as nombre_ubicacion, id_categoria, c.nombre as nombre_categoria
    FROM historia AS h
    INNER JOIN ubicacion AS ct ON h.id_ubicacion = ct.id
    INNER JOIN categoria_historia AS c ON h.id_categoria = c.id
    WHERE h.titulo = %s
"""

GET_HISTORIA_BY_UBICACION = """
    SELECT h.id, h.titulo, h.descripcion, h.fecha_inicio, h.fecha_fin, h.imagen, h.id_ubicacion, ct.nombre as nombre_ubicacion, id_categoria, c.nombre as nombre_categoria
    FROM historia AS h
    INNER JOIN ubicacion AS ct ON h.id_ubicacion = ct.id
    INNER JOIN categoria_historia AS c ON h.id_categoria = c.id
    WHERE ct.nombre = %s
"""

GET_HISTORIA_BY_CATEGORIA = """
    SELECT h.id, h.titulo, h.descripcion, h.fecha_inicio, h.fecha_fin, h.imagen, h.id_ubicacion, ct.nombre as nombre_ubicacion, id_categoria, c.nombre as nombre_categoria
    FROM historia AS h
    INNER JOIN ubicacion AS ct ON h.id_ubicacion = ct.id
    INNER JOIN categoria_historia AS c ON h.id_categoria = c.id
    WHERE c.nombre = %s
"""

CREATE_HISTORIA = """
    INSERT INTO historia (titulo, descripcion, fecha_inicio, fecha_fin, imagen, id_ubicacion, id_categoria)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_HISTORIA = """
    UPDATE historia
    SET titulo = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s, imagen = %s, id_ubicacion = %s, id_categoria = %s
    WHERE id = %s
"""

DELETE_HISTORIA = """
    DELETE FROM historia WHERE id = %s
"""
