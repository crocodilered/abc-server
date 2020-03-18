
INSERT_SQL = '''
    INSERT INTO sign (
        name,
        email,
        profession,
        comments,
        created,
        updated,
        secret_key,
        published
    ) VALUES (
        %s, %s, %s, %s,
        NOW(), NOW(), %s, NULL
    )
    RETURNING id
'''

SELECT_SQL = '''
    SELECT
        id,
        name,
        email,
        profession,
        comments,
        created,
        updated,
        secret_key,
        published,
        serial
    FROM sign
    WHERE {conditions} AND 1 = 1
    ORDER BY published 
    LIMIT %s
    OFFSET %s
'''

LOCK_SQL = '''
    LOCK TABLE sign IN SHARE MODE
'''

NEXT_SERIAL_SQL = '''
    SELECT CASE 
        WHEN MAX(serial) IS NULL THEN 1 
        ELSE MAX(serial) + 1 END FROM sign
'''

PUBLISH_SQL = '''
    UPDATE sign SET
        published = %s,
        serial = %s
    WHERE secret_key = %s
'''

GET_COUNT_SQL = '''
    SELECT COUNT(id) FROM sign WHERE published IS NOT NULL
'''
