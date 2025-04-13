GET_ALL_BIBLIOTECAS = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
"""

GET_BIBLIOTECA_BY_ID = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
    WHERE b.id = %s
"""

GET_BIBLIOTECA_BY_TITLE = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
    WHERE b.titulo = %s
"""

GET_BIBLIOTECA_BY_CATEGORIA = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
    WHERE c.tipo = %s
"""

GET_BIBLIOTECA_BY_AUTOR = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
    WHERE b.autor = %s
"""

GET_BIBLIOTECA_BY_FECHA = """
    SELECT b.id, b.titulo, b.autor, b.imagen, b.fecha_publicacion, b.edicion, 
           b.id_tipo, b.fuente, b.enlace, b.id_usuario, c.tipo
    FROM biblioteca AS b
    INNER JOIN tipo_documento AS c ON b.id_tipo = c.id_tipo
    WHERE b.fecha_publicacion = %s
"""

CREATE_BIBLIOTECA = """
    INSERT INTO biblioteca (titulo, autor, imagen, fecha_publicacion, edicion, 
                            id_usuario, id_tipo, fuente, enlace)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_BIBLIOTECA = """
    UPDATE biblioteca
    SET titulo = %s, autor = %s, imagen = %s, fecha_publicacion = %s, edicion = %s, 
        id_tipo = %s, fuente = %s, enlace = %s, id_usuario = %s
    WHERE id = %s
"""

DELETE_BIBLIOTECA = """
    DELETE FROM biblioteca WHERE id = %s
"""