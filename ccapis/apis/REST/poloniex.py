"""
Contains all API Client sub-classes, which store exchange specific details
and feature the respective exchanges authentication method (sign()).
"""
# Import Built-ins
import logging
import hashlib
import hmac
import urllib
import urllib.parse

# Import Homebrew
from ccapis.apis.rest import RESTAPIClient


log = logging.getLogger(__name__)


class PoloniexREST(RESTAPIClient):
    def __init__(self, key=None, secret=None, api_version=None,
                 url='https://poloniex.com', timeout=5):
        super(PoloniexREST, self).__init__(url, api_version=api_version,
                                           key=key, secret=secret,
                                           timeout=timeout)

    def sign(self, uri, endpoint, endpoint_path, method_verb, *args, **kwargs):
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        params['nonce'] = self.nonce()
        payload = params

        data = urllib.parse.urlencode(payload).encode('utf-8')
        h = hmac.new(self.secret.encode('utf-8'), data, hashlib.sha512)
        signature = h.hexdigest()

        headers = {
            'Key': self.key,
            'Sign': signature
        }

        return uri, {'headers': headers, 'data': params}

    async def public_query(self, endpoint, **kwargs):
        return await self.query('GET', 'public?command=' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('POST', endpoint,
                          authenticate=True, **kwargs)

    def get_pair(self, base, count):
        return count + '_' + base
