# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from ccapis.formatters.base import Formatter


log = logging.getLogger(__name__)


class BitfinexFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], None, None,
                data['last_price'], data['volume'], data['timestamp'])

    @staticmethod
    def order(data, *args, **kwargs):
        try:
            return data['order_id']
        except KeyError:
            return False

    @staticmethod
    def cancel(data, *args, **kwargs):
        return True if 'message' not in data else False

    @staticmethod
    def order_status(data, *args, **kwargs):
        return data['is_live']
