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
        if 'user_id' in kwargs:
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


    def query(self, method_verb, endpoint, authenticate=False,
              *args, **kwargs):
        """
        Queries exchange using given data. Defaults to unauthenticated query.
        :param method_verb: valid request type (PUT, GET, POST etc)
        :param endpoint: endpoint path for the resource to query, sans the url &
                         API version (i.e. '/btcusd/ticker/').
        :param authenticate: Bool to determine whether or not a signature is
                             required.
        :param args: Optional args for requests.request()
        :param kwargs: Optional Kwargs for self.sign() and requests.request()
        :return: request.response() obj
        """

        endpoint_path = '/' + endpoint

        url = self.uri + endpoint_path
        if authenticate:  # sign off kwargs and url before sending request
            endpoint_path = '/' + self.version + '/' + endpoint
            url, request_kwargs = self.sign(url, endpoint, endpoint_path,
                                            method_verb, *args, **kwargs)
        else:
            request_kwargs = kwargs
        log.debug("Making request to: %s, kwargs: %s", url, request_kwargs)
        r = self.api_request(method_verb, url, timeout=self.timeout,
                             **request_kwargs)
        log.debug("Made %s request made to %s, with headers %s and body %s. "
                  "Status code %s", r.request.method,
                  r.request.url, r.request.headers,
                  r.request.body, r.status_code)
        return r


    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)
