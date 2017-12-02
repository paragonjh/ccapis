"""
https://api.bithumb.com
"""

# Import Built-Ins
import logging

# Import Third-Party

# Import  Homebrew
from ccapis.apis.REST import BithumbREST
from ccapis.formatters.base import return_api_response
from ccapis.formatters.bithumb import BithumbFormatter as fmt

# Init Logging Facilities
log = logging.getLogger(__name__)


class Bithumb(BithumbREST):
    def __init__(self, key='', secret='', key_file=''):
        super(Bithumb, self).__init__(key, secret)
        if key_file:
            self.load_key(key_file)

    """
    Bithumb Standardized Methods
    """

    @return_api_response(fmt.ticker)
    def ticker(self, base, counter=None):
        return self.public_query('ticker', params=base)

    @return_api_response(fmt.order_book)
    #parameter: {'count':10(default 10)}
    def order_book(self, pair, **kwargs):
        orderBookURL = 'orderbook/'+pair
        q = {}
        q.update(kwargs)
        return self.public_query(orderBookURL, params=q)

    # This information is contained in Ticker API
    # @return_api_response(fmt.trades)
    # def trades(self, pair, **kwargs):
    #     q = {'market': pair}
    #     q.update(kwargs)
    #     return self.public_query('getmarkethistory', params=q)

    def _place_order(self, pair, size, price, side, **kwargs):
        q = {'order_currency': pair, 'units': size, 'price': price, 'side': side,
             'Payment_currency':'KRW'}
        q.update(kwargs)
        return self.private_query('trade/place', params=q)

    def _place_order_market(self, pair, size, side, **kwargs):
        q = {'currency': pair, 'units': size}
        q.update(kwargs)
        if side == 'bid':
            return self.private_query('trade/market_buy', params=q)
        else:
            return self.private_query('trade/market_sell', params=q)

    @return_api_response(fmt.order)
    def bid(self, pair, price=0, size=0, market=False, **kwargs):
        if market:
            return self._place_order_market(pair, float(size), 'bid', **kwargs)
        else:
            return self._place_order(pair, float(size), int(price), 'bid', **kwargs)

    @return_api_response(fmt.order)
    def ask(self, pair, price=0, size=0, market=False, **kwargs):
        if market:
            return self._place_order_market(pair, float(size), 'ask', **kwargs)
        else:
            return self._place_order(pair, float(size), int(price), 'ask', **kwargs)

    @return_api_response(fmt.cancel)
    #Parameter: {'order_id': String, 'type': 'bid' or 'ask', 'currency': 'BTC','ETH'...}
    def cancel_order(self, txid, **kwargs):
        q = {'order_id': txid}
        q.update(kwargs)
        return self.private_query('trade/cancel', params=q)

    @return_api_response(fmt.order_status)
    #parameter: {'order_id': String, 'type': 'bid or 'ask', 'currency': 'BTC','ETH'... ,
    #             'count':100(default:100), 'after':Int(Unit TimeStamp)}
    def order(self, txid, **kwargs):
        q = {'order_id': txid}
        q.update(kwargs)
        return self.private_query('info/orders', params=q)

    @return_api_response(fmt.balance)
    # parameter: {'currency': 'BTC' or 'EHT'.. (Default: 'BTC')}
    def balance(self,  **kwargs):
        q = {}
        q.update(kwargs)
        return self.private_query('info/balance')

    @return_api_response(fmt.withdraw)
    # parameter: {'units': float, 'address': String, 'currency': 'BTC', 'ETH'...}
    def withdraw(self, size, tar_addr, **kwargs):
        q = {'units': size, 'address': tar_addr}
        q.update(kwargs)
        return self.private_query('trade/btc_withdrawal', params=q)

    @return_api_response(fmt.deposit)
    def deposit_address(self, pair, **kwargs):
        q = {'currency':pair}
        q.update(kwargs)
        return self.private_query('info/wallet_address', params=kwargs)

    """
    Exchange Specific Methods
    """

    @return_api_response(None)
    def pairs(self):
        return self.public_query('getmarkets')

    @return_api_response(None)
    def currencies(self):
        return self.public_query('getcurrencies')

    @return_api_response(None)
    def statistics(self, pair=None):
        if pair:
            return self.public_query('getmarketsummary', params={'market': pair})
        else:
            return self.public_query('getmarketsummaries')
