GET_NOTIFICACION_BY_ID = """
    SELECT u.id_usuario,e.id AS id_evento,e.nombre As nombre_evento
    FROM USUARIO_EVENTO u
    INNER JOIN evento e ON u.id_evento = e.id
    WHERE u.id_usuario = %s
    """
