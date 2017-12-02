# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from ccapis.formatters.base import Formatter

log = logging.getLogger(__name__)


class CoinoneFormatter(Formatter):
    pass
    # @staticmethod
    # def ticker(data, *args, **kwargs):
    #     data = data['data']
    #     return (data['buy_price'], data['sell_price'], data['max_price'], data['min_price'],
    #             data['opening_price'], data['opening_price'],data['buy_price'], data['units_traded'], data['date'])

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