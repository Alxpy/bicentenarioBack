GET_TIPO_DOCUMENTO_BY_ID = """
    SELECT td.id,td.tipo
    FROM tipo_documento as td
    WHERE td.id = %s
"""

GET_ALL_TIPOS_DOCUMENTO = """
    SELECT td.id,td.tipo
    FROM tipo_documento as td
"""

CREATE_TIPO_DOCUMENTO = """
    INSERT INTO tipo_documento (tipo)
    VALUES (%s)
    """
UPDATE_TIPO_DOCUMENTO = """
    UPDATE tipo_documento
    SET tipo = %s
    WHERE id = %s
    """

DELETE_TIPO_DOCUMENTO = """
    DELETE FROM tipo_documento 
    WHERE id = %s
    """

