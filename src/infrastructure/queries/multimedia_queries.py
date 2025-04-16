GET_ALL_MULTIMEDIA = """
    SELECT m.id, m.enlace, m.tipo
    FROM multimedia m
"""
GET_MULTIMEDIA_BY_ID = """
    SELECT m.id, m.enlace, m.tipo
    FROM multimedia m
    WHERE m.id = %s
"""
CREATE_MULTIMEDIA = """
    INSERT INTO multimedia (enlace, tipo)
    VALUES (%s, %s)
"""
UPDATE_MULTIMEDIA = """
    UPDATE multimedia
    SET enlace = %s, tipo =%s
    WHERE id = %s
    """
DELETE_MULTIMEDIA = """
    DELETE FROM multimedia
    WHERE id = %s
"""
