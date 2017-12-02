# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from ccapis.formatters.base import Formatter

log = logging.getLogger(__name__)


class KorbitFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        # [bid_price, ask_price, high, low, open, close, last, 24h_vol, ts]
        return (None, None, None, None, None, None, data['last'], None, data['timestamp'])

    # @staticmethod
    # def order(data, *args, **kwargs):
    #     if data['status'] == '0000':
    #         return data['order_id']
    #     else:
    #         return False
    #
    # @staticmethod
    # def order_book(data, *args, **kwargs):
    #     if data['status'] == '0000':
    #         return data['data']
    #     else:
    #         return None
    #
    # @staticmethod
    # def cancel(data, *args, **kwargs):
    #     return True if data['status'] == '0000' else False
