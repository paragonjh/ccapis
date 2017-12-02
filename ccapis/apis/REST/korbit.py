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
import datetime

# Import Homebrew
from ccapis.apis.rest import RESTAPIClient


log = logging.getLogger(__name__)


class KorbitREST(RESTAPIClient):
    def __init__(self, key=None, secret=None, api_version='v1',
                 url='https://api.korbit.co.kr', timeout=5, **kwargs):
        self.id = kwargs['user_id']
        self.password = kwargs['password']
        self.expire = 3600
        self.access_token = ''
        self.refresh_token = ''
        self.access_time = 0
        super(KorbitREST, self).__init__(url, api_version=api_version,
                                           key=key, secret=secret,
                                           timeout=timeout)

    def authentication(self):
        params = {
            'client_id': self.key,
            'client_secret': self.secret,
            'username': self.id,
            'passworkd': self.password,
            'grant_type': 'password'
        }

        data =  urllib.parse.urlencode(params)

        self.access_time = datetime.datetime.now()

        return self.api_request('POST', 'https://api.korbit.co.kr/v1/oauth2/access_token', data=data)

    def reauthentication(self):
        params = {
            'client_id': self.key,
            'client_secret': self.secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }

        data =  urllib.parse.urlencode(params)

        return self.api_request('POST', 'https://api.korbit.co.kr/v1/oauth2/access_token', data=data)

    def sign(self, url, endpoint, endpoint_path, method_verb, *args, **kwargs):
        __nonce = self.nonce()
        try:
            params = kwargs['params']
        except KeyError:
            params = {}

        params['nonce'] = __nonce
        current_time = datetime.datetime.now()
        if self.access_time is 0 :
            response = self.authentication()

            self.expire = response['expires_in']
            __token_type = response['token_type']
            self.refresh_token = response['refresh_token']
            self.access_token = response['access_token']

        else :
            time_delta = current_time - self.access_time
            if time_delta.total_seconds()-600 > self.expire:
                response = self.reauthentication()

                self.expire = response['expires_in']
                __token_type = response['token_type']
                self.refresh_token = response['refresh_token']
                self.access_token = response['access_token']

        token = __token_type + chr(0) + self.access_token
        headers = {
            'Authorization': token
        }

        return url, {'headers': headers}

    def public_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, **kwargs)

    def private_query(self, endpoint, **kwargs):
        return self.query('GET', endpoint, authenticate=True, **kwargs)

    def get_pair(self, base, count):
        base = base.lower()
        count = count.lower()
        return base + '_' + count
