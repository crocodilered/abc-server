from pymemcache.client import base
from flask import jsonify


__all__ = ['Memcached']


class Memcached(object):
    """
    Proxy to memcached client to unify codebase.
    get() method no need coz of nginx can get data from memcached itself.
    """
    _client = None

    def __init__(self, conf):
        if (
            conf.get('host') and
            conf.get('port')
        ):
            _client = base.Client((conf['host'], conf['port']))
            _client.default_noreply = True

    def set(self, key, content):
        if self._client:
            self._client.set(key, jsonify(content))

        return content

    def delete_many(self, keys):
        if self._client:
            self._client.delete_many(keys)
