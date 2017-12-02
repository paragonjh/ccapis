# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from ccapis.formatters.base import Formatter


log = logging.getLogger(__name__)


class PoloniexFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        data = data[args[1]]
        return (data['highestBid'], data['lowestAsk'], None, None, None, None,
                data['last'], None, None)

    @staticmethod
    def order(data, *args, **kwargs):
        try:
            return data['orderNumber']
        except KeyError:
            return False

    @staticmethod
    def cancel(data, *args, **kwargs):
        return True if data['success'] else False
