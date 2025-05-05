GET_ALL_PATROCINADORES = """
    SELECT p.id, p.nombre, p.imagen, p.contacto
    FROM patrosinador p
    """

CREATE_PATROCINADOR = """
    INSERT INTO patrosinador (nombre, imagen, contacto)
    VALUES (%s, %s, %s)
"""
    