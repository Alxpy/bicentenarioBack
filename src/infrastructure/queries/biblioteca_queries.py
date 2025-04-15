GET_ALL_BIBLIOTECAS = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
"""

GET_BIBLIOTECA_BY_ID = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
    WHERE b.id = %s
"""
GET_BIBLIOTECA_BY_TITLE= """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
    WHERE b.titulo = %s
"""
GET_BIBLIOTECA_BY_CATEGORIA = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
    WHERE c.tipo = %s
    """
GET_BIBLIOTECA_BY_AUTOR = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
    WHERE b.autor = %s
"""

GET_BIBLIOTECA_BY_FECHA = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion,b.id_tipo, b.fuente,b.enlace,c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id
    WHERE b.fecha_publicacion = %s
"""

CREATE_BIBLIOTECA = """
    INSERT INTO biblioteca (titulo, autor, imagen, fecha_publicacion, edicion, id_tipo, fuente, enlace)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_BIBLIOTECA = """
    UPDATE biblioteca
    SET titulo = %s, autor = %s, imagen = %s, fecha_publicacion = %s, edicion = %s, id_tipo = %s, fuente = %s, enlace = %s
    WHERE id = %s    
"""

DELETE_BIBLIOTECA = """
    DELETE FROM biblioteca WHERE id = %s
"""