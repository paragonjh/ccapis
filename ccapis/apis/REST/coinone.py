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
import json
import hmac

# Import Homebrew
from ccapis.apis.rest import RESTAPIClient


log = logging.getLogger(__name__)


class CoinoneREST(RESTAPIClient):
    def __init__(self, key=None, secret=None, api_version='v2',
                 url='https://api.coinone.co.kr', timeout=5, **kwargs):
        self.id = kwargs['user_id']
        super(CoinoneREST, self).__init__(url, api_version=api_version,
                                           key=key, secret=secret,
                                           timeout=timeout)

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):
        __nonce = self.nonce()

        data = {
            'nonce': int(__nonce)
        }
        payload = base64.b64encode(json.dumps(data))

        h = hmac.new(str(self.secret).upper(), str(payload), hashlib.sha512)
        signature = h.hexdigest()

        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': payload,
            'X-COINONE-SIGNATURE': signature

        }

        return url, {'headers': headers}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)
