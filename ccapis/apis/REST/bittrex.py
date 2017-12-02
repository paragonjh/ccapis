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


class BittrexREST(RESTAPIClient):
    def __init__(self, key=None, secret=None, api_version='v1.1',
                 url='https://bittrex.com/api', timeout=5):
        super(BittrexREST, self).__init__(url, api_version=api_version, key=key,
                                          secret=secret, timeout=timeout)

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):

        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        nonce = self.nonce()

        req_string = endpoint_path + '?apikey=' + self.key + "&nonce=" + nonce + '&'
        req_string += urllib.parse.urlencode(params)

        data = (self.uri + req_string).encode('utf-8')
        h = hmac.new(self.secret.encode('utf-8'), data, hashlib.sha512)
        signature = h.hexdigest()

        headers = {
            "apisign": signature
        }

        return self.uri + req_string, {'headers': headers, 'params': {}}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'public/' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)

    def get_pair(self, base, count):
        return count + '-' + base
