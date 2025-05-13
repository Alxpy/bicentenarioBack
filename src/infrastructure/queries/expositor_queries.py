GET_ALL_EXP="""
SELECT 
    e.id,
    e.nombre
FROM expositor AS e
"""
CREATE_EXP="""
INSERT INTO expositor (nombre)
VALUES (%s)
"""

CREATE_EXP_EVENT="""
INSERT INTO even_expo (id_event, id_expo)
VALUES (%s, %s)
"""

GET_ALL_EXP_BY_EVENT="""
SELECT 
    e.id,
    e.nombre
FROM expositor AS e
JOIN even_expo AS ee ON e.id = ee.id_expo
WHERE ee.id_event = %s
""" 

DELETE_EXP_EVENT="""
DELETE FROM even_expo
WHERE id_event = %s AND id_expo = %s
"""