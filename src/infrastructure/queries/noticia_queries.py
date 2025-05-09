GET_NOTICIA_BY_ID = """
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, 
           n.id_categoria AS id_Categoria, 
           n.id_usuario AS id_usuario, 
           n.fecha_publicacion, 
           c.nombre_categoria,
              u.nombre AS nombre_usuario
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.id_categoria = c.id
    INNER JOIN usuario AS u ON n.id_usuario = u.id
    WHERE n.id = %s
"""

GET_ALL_NOTICIAS = """
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, 
           n.id_categoria AS id_Categoria, 
           n.id_usuario AS id_usuario, 
           n.fecha_publicacion, 
           c.nombre_categoria,
            u.nombre AS nombre_usuario
           
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.id_categoria = c.id
    INNER JOIN usuario AS u ON n.id_usuario = u.id
"""

GET_NOTICIA_BY_FECHA = """ 
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, 
           n.id_categoria AS id_Categoria, 
           n.id_usuario AS id_usuario, 
           n.fecha_publicacion, 
           c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.id_categoria = c.id
    WHERE DATE(n.fecha_publicacion) = %s
"""

GET_NOTICIA_BY_CATEGORIA = """
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, 
           n.id_categoria AS id_Categoria, 
           n.id_usuario AS id_usuario, 
           n.fecha_publicacion, 
           c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.id_categoria = c.id
    WHERE c.nombre_categoria = %s
"""

GET_NOTICIA_BY_TITLE = """
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, 
           n.id_categoria AS id_Categoria, 
           n.id_usuario AS id_usuario, 
           n.fecha_publicacion, 
           c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.id_categoria = c.id
    WHERE n.titulo = %s
"""

CREATE_NOTICIA = """ 
    INSERT INTO noticia (titulo, resumen, contenido, imagen, id_categoria, id_usuario, fecha_publicacion)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_NOTICIA = """
    UPDATE noticia 
    SET titulo = %s, resumen = %s, contenido = %s, imagen = %s, 
        id_categoria = %s, fecha_publicacion = %s
    WHERE id = %s
"""

DELETE_NOTICIA = """ 
    DELETE FROM noticia WHERE id = %s
"""
