import psycopg2
import datetime

from flask import Flask, request
from flask_cors import CORS

import config
from sendmail import send_confirmation
from memcached import Memcached

from models import Sign
from services import SignsService


app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(**config.PG_SQL)

memcached = Memcached(config.MEMCACHED)

app_page_size = config.APP['page-size']


@app.route('/signs/list/<offset>/', methods=['GET'])
def signs_list(offset=0):
    """
    GET list signs by 100 items, started with offset.
    """
    signs = SignsService.list(conn, int(offset) * app_page_size)
    response = {'list': [sign.serialize() for sign in signs]}

    # Discuss to use memcached as decorator.
    # Discuss to use memcached as decorator.
    return memcached.set(f'/signs/list/{offset}/', response)


@app.route('/signs/filter/', methods=['GET'])
def signs_filter():
    """
    GET Filter signs with given name part.
    """
    name = request.args.get('name')
    signs = SignsService.filter(conn, name__like=name)
    return {'list': [sign.serialize() for sign in signs]}


@app.route('/signs/generate/', methods=['GET'])
def signs_generate():
    """
    GET Generate test data.
    """
    import names
    records_count = 5034

    for i in range(0, records_count):
        name = names.get_full_name()

        try:
            sign = Sign(
                name=name,
                email=name.replace(' ', '.') + '@mail.com',
                published=datetime.datetime.now()
            )

            SignsService.create(conn, sign)
            SignsService.publish(conn, sign)
        except psycopg2.errors.UniqueViolation:
            conn.rollback()

    return {'message': f'Done for {records_count} records.'}, 201


@app.route('/signs/create/', methods=['POST'])
def signs_create():
    """
    POST Create sign.
    """
    j = request.json

    sign = Sign(
        name=j['name'],
        email=j['email'],
        profession=j['profession'],
        comments=j['comments'],
    )

    SignsService.create(conn, sign)

    send_confirmation(sign)

    return {}, 201


@app.route('/signs/publish/', methods=['PUT'])
def signs_publish():
    """
    GET Publish the sign with given @secret_key in query.
    """
    secret_key = request.json.get('secret_key')

    signs = SignsService.filter(conn, secret_key=secret_key)

    if (
        signs and
        signs[0].published is None
    ):
        sign = SignsService.publish(conn, signs[0])

        # Reset cache: statistics endpoint and last page
        if memcached:
            last_page_offset = SignsService.count(conn) / app_page_size + 1
            memcached.delete_many([
                '/signs/statistics/',
                f'/signs/list/{last_page_offset}/'
            ])

        return {'sign': sign.serialize()}

    return '', 404


@app.route('/signs/statistics/', methods=['GET'])
def signs_statistics():
    """
    GET Return system statistics.
    """
    signs_count = SignsService.count(conn)
    response = {'signs_count': signs_count}

    return memcached.set('/signs/statistics/', response)


if __name__ == '__main__':
    app.run(
        port=config.FLASK.get('port'),
        debug=config.FLASK.get('debug')
    )
