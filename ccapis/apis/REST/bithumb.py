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
import urllib

# Import Homebrew
from ccapis.apis.rest import RESTAPIClient


log = logging.getLogger(__name__)


class BithumbREST(RESTAPIClient):
    def __init__(self, user_id='', key=None, secret=None, api_version=None,
                 url='https://api.bithumb.com', timeout=5):
        self.id = user_id
        super(BithumbREST, self).__init__(url, api_version=api_version,
                                           key=key, secret=secret,
                                           timeout=timeout)

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):
        __endpoint = {
            'endpoint': endpoint
        }
        try:
            __uri = dict(endpoint, **kwargs['params'])
        except KeyError:
            __uri = endpoint

        __nonce = self.nonce()
        data = endpoint+ chr(0) + urllib.parse.urlencode(__uri) + chr(0) + __nonce
        data = data.encode('utf-8')

        h = hmac.new(bytes(self.secret.encode('utf-8')), data, hashlib.sha512)
        signature = base64.b64encode( h.hexdigest().encode('utf-8') ).decode('utf-8')

        headers = {
            'Api-Key': self.key,
            'Api-Sign': signature,
            'Api-Nonce': __nonce
        }

        return url , {'headers': headers}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', 'public/' + endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)

    # endpoint_item_array = {
    #     "endpoint": endpoint
    # };
    #
    # uri_array = dict(endpoint_item_array, **rgParams);  # Concatenate the two arrays.
    #
    # str_data = urllib.parse.urlencode(uri_array);
    # data = endpoint + chr(0) + str_data + chr(0) + nonce;
    # utf8_data = data.encode('utf-8');
    #
    # key = self.api_secret;
    # utf8_key = key.encode('utf-8');
    #
    # h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512);
    # hex_output = h.hexdigest();
    # utf8_hex_output = hex_output.encode('utf-8');
    #
    # api_sign = base64.b64encode(utf8_hex_output);
    # utf8_api_sign = api_sign.decode('utf-8');

#curl_handle.setopt(curl_handle.HTTPHEADER, ['Api-Key: ' + self.api_key, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce]);
