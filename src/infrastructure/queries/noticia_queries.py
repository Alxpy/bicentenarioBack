GET_NOTICIA_BY_ID = """
    SELECT n.id,n.titulo,n.resumen,n.contenido,n.imagen,n.idCategoria,n.fecha_publicacion,c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.idCategoria = c.id
    WHERE n.id = %s
"""

GET_ALL_NOTICIAS = """
    SELECT n.id,n.titulo,n.resumen,n.contenido,n.imagen,n.idCategoria,n.fecha_publicacion,c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.idCategoria = c.id
"""

GET_NOTICIA_BY_FECHA = """ 
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen,n.idCategoria, n.fecha_publicacion, c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.idCategoria = c.id
    WHERE DATE(n.fecha_publicacion) = %s;

"""

GET_NOTICIA_BY_CATEGORIA = """
    SELECT n.id, n.titulo, n.resumen, n.contenido, n.imagen, n.idCategoria, n.fecha_publicacion, c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.idCategoria = c.id
    WHERE c.nombre_categoria = %s;

"""
GET_NOTICIA_BY_TITLE = """
    SELECT n.id,n.titulo,n.resumen,n.contenido,n.imagen,n.idCategoria,n.fecha_publicacion,c.nombre_categoria
    FROM noticia AS n
    INNER JOIN categorianoticia AS c ON n.idCategoria = c.id
    WHERE n.titulo = %s

"""
CREATE_NOTICIA = """ 
    INSERT INTO noticia (titulo,resumen,contenido,imagen,idCategoria,fecha_publicacion)
    VALUES (%s,%s,%s,%s,%s,%s)
"""
UPDATE_NOTICIA = """
    UPDATE noticia 
    SET titulo = %s, resumen = %s, contenido = %s, imagen = %s, idCategoria = %s, fecha_publicacion = %s
    WHERE id = %s
"""
DELETE_NOTICIA = """ 
    DELETE FROM noticia WHERE id = %s
"""