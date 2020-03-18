import uuid
from datetime import datetime

from models import Sign
from sql import (
    SELECT_SQL,
    INSERT_SQL,
    LOCK_SQL,
    NEXT_SERIAL_SQL,
    PUBLISH_SQL,
    GET_COUNT_SQL
)

from config import APP


class SignsService:

    @staticmethod
    def list(conn, offset=0, count=APP['page-size']):
        sql = SELECT_SQL.format(
            conditions='published IS NOT NULL'
        )

        cursor = conn.cursor()
        cursor.execute(sql, [count, offset])
        rows = cursor.fetchall()

        return [Sign.from_row(row) for row in rows]

    @staticmethod
    def filter(conn, offset=0, count=APP['page-size'], **kwargs):
        conditions = []
        params = []

        if 'secret_key' in kwargs:
            secret_key = kwargs.get('secret_key')
            conditions.append('secret_key = %s')
            params.append(secret_key)

        if 'name__like' in kwargs:
            name__like = '%{}%'.format(kwargs.get('name__like'))
            conditions.append('UPPER(name) LIKE UPPER(%s)')
            params.append(name__like)

        params.append(count)
        params.append(offset)

        sql = SELECT_SQL.format(conditions=' AND '.join(conditions))

        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        return [Sign.from_row(row) for row in rows]

    @staticmethod
    def create(conn, sign):
        cursor = conn.cursor()

        sign.secret_key = uuid.uuid4().hex

        payload = (
            sign.name,
            sign.email,
            sign.profession,
            sign.comments,
            sign.secret_key,
        )

        cursor.execute(INSERT_SQL, payload)
        sign.id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()

        return sign

    @staticmethod
    def publish(conn, sign):
        cursor = conn.cursor()

        cursor.execute(LOCK_SQL)
        cursor.execute(NEXT_SERIAL_SQL)

        sign.serial = cursor.fetchone()
        sign.published = datetime.now()

        cursor.execute(PUBLISH_SQL, (
            sign.published,
            sign.serial,
            sign.secret_key,
        ))

        conn.commit()
        cursor.close()

        return sign

    @staticmethod
    def count(conn):
        cursor = conn.cursor()
        cursor.execute(GET_COUNT_SQL)
        signs_count = cursor.fetchone()[0]
        cursor.close()
        return signs_count
