"""
Base Class for formatters. Does nothing with passed data by default;
Children should implement formatters as necessary
"""

# Import Built-Ins
import logging
from abc import ABCMeta, abstractmethod
import json
from functools import wraps
# Import Third-Party
import requests

# Import Homebrew

# Init Logging Facilities


log = logging.getLogger(__name__)


def return_api_response(formatter=None):
    """
    Decorator, which Applies the referenced formatter (if available) to the
    function output and adds it to the APIResponse Object's `formatted`
    attribute.
    :param formatter: ccapis.formatters.Formatter() obj
    :return: ccapis.api.response.RESTAPIResponse()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print (func)
            print (args)
            print (kwargs)
            try:
                r = func(*args, **kwargs)
            except Exception:
                log.exception("return_api_response(): Error during call to %s(%s, %s)",
                              func.__name__, args, kwargs)
                raise

            # Check Status
            try:
                r.raise_for_status()
            except requests.HTTPError:
                log.exception("return_api_response: HTTPError for url %s",
                              r.request.url)

            #  Verify json data
            try:
                data = r.json()
            except json.JSONDecodeError:
                log.error('return_api_response: Error while parsing json. '
                          'Request url was: %s, result is: '
                          '%s', r.request.url, r.text)
                data = None
            except Exception:
                log.exception("return_api_response(): Unexpected error while parsing "
                              "json from %s", r.request.url)
                raise

            # Format, if available
            if formatter is not None and data:
                try:
                    r.formatted = formatter(data, *args, **kwargs)
                except Exception:
                    log.exception("Error while applying formatter!")

            return r

        return wrapper
    return decorator



class Formatter:
    """
    ABC Class to provide formatters for `bitex.utils.return_api_response()`.
    """
    def __init__(self):
        pass

    @staticmethod
    def format_pair(input_pair):
        """
        Returns the pair properly formatted for the exchange's API.
        :param input_pair: str
        :return: str
        """
        return input_pair

    @staticmethod
    def ticker(data, *args, **kwargs):
        """
        Returns list of ticker data in following format:
            [bid_price, ask_price, high, low, open, close, last, 24h_vol, ts]
        :param data: requests.response() obj
        :param args:
            args[0] 1st argument of ticker, interface object,
            args[1] 2nd argument of ticker, base,
            args[2] 3rd argument of ticker, counter
        :param kwargs:
        :return: list
        """
        return data

    @staticmethod
    def order_book(data, *args, **kwargs):
        """
        Returns dict of lists of lists of quotes in format [ts, price, size]
        ex.:
            {'bids': [['1480941692', '0.014', '10'],
                      ['1480941690', '0.013', '0.66'],
                      ['1480941688', '0.012', '3']],
             'asks': [['1480941691', '0.015', '1'],
                      ['1480941650', '0.016', '0.67'],
                      ['1480941678', '0.017', '23']]}
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: dict
        """
        return data

    @staticmethod
    def trades(data, *args, **kwargs):
        """
        Returns list of trades in format [ts, price, size, side]
        ex.:
            [['1480941692', '0.014', '10', 'sell'],
            ['1480941690', '0.013', '0.66', 'buy'],
            ['1480941688', '0.012', '3', 'buy']]
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: list
        """
        return data

    @staticmethod
    def order(data, *args, **kwargs):
        """
        Returns the order id as str if successful, else ""
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: str
        """
        return data

    @staticmethod
    def order_status(data, *args, **kwargs):
        """
        Returns True if it exists, False if it doesn't exist
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: bool
        """
        return data

    @staticmethod
    def cancel(data, *args, **kwargs):
        """
        returns True if it was cancelled successfully, else False
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: bool
        """
        return data

    @staticmethod
    def balance(data, *args, **kwargs):
        """
        Returns dict of available balances, with currency names as keys - this ignores
        any amount already involved in a trade (i.e. margin)
        ex.:
            {'BTC': '12.04', 'LTC': '444.12'}
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: dict
        """
        return data

    @staticmethod
    def withdraw(data, *args, **kwargs):
        """
        Returns a list giving details of success and transaction details, or failure
        and reason thererof
        ex.:
            [True, currency, amount, target_address, txid]
            [False, 'Reason for failure/ error message']
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: list
        """
        return data

    @staticmethod
    def deposit(data, *args, **kwargs):
        """
        Returns deposit address as str
        :param data: requests.response() obj
        :param args:
        :param kwargs:
        :return: str
        """
        return data
