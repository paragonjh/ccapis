"""
Contains all API Client sub-classes, which store exchange specific details
and feature the respective exchanges authentication method (sign()).
"""
# Import Built-ins
import sys
import time
import math
import base64
import logging
import hashlib
import hmac

# Import Homebrew
from ccapis.apis.REST.api import RESTAPIResponse


log = logging.getLogger(__name__)


class BithumbREST(RESTAPIResponse):
    def __init__(self, user_id='', key=None, secret=None, api_version=None,
                 url='https://api.bithumb.com', timeout=5):
        self.id = user_id
        super(BithumbREST, self).__init__(url, api_version=api_version,
                                           key=key, secret=secret,
                                           timeout=timeout)

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):
        nonce = self.nonce()
        message = nonce + self.id + self.key

        signature = hmac.new(self.secret.encode(), message.encode(),
                             hashlib.sha256)
        signature = signature.hexdigest().upper()

        try:
            req = kwargs['params']
        except KeyError:
            req = {}
        req['key'] = self.key
        req['nonce'] = nonce
        req['signature'] = signature
        return url, {'data': req}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'public/' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)
