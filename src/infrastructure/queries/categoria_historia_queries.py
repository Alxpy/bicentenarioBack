GET_ALL_CATEGORIA_HISTORIA = """
SELECT ch.id, ch.nombre, ch.descripcion
FROM categoria_historia ch
"""

GET_CATEGORIA_HISTORIA_BY_ID = """
SELECT ch.id, ch.nombre, ch.descripcion
FROM categoria_historia ch
WHERE ch.id = %s
"""

CREATE_CATEGORIA_HISTORIA = """
INSERT INTO categoria_historia (nombre, descripcion)
VALUES (%s, %s)
"""
UPDATE_CATEGORIA_HISTORIA = """
UPDATE categoria_historia
SET nombre = %s, descripcion = %s
WHERE id = %s
"""
DELETE_CATEGORIA_HISTORIA = """ DELETE FROM categoria_historia WHERE id = %s """
