GET_CATEGORIA_NOTICIA_BY_ID = """
    SELECT cn.id,cn.nombre_categoria
    FROM categorianoticia as cn
    WHERE cn.id = %s
""" 

GET_ALL_CATEGORIAS_NOTICIA = """
    SELECT cn.id,cn.nombre_categoria
    FROM categorianoticia as cn
"""

CREATE_CATEGORIA_NOTICIA = """
    INSERT INTO categorianoticia (nombre_categoria)
    VALUES (%s)
"""

UPDATE_CATEGORIA_NOTICIA = """
    UPDATE categorianoticia 
    SET nombre_categoria = %s
    WHERE id = %s
"""

DELETE_CATEGORIA_NOTICIA_BY_ID = "DELETE FROM categorianoticia WHERE id = %s"