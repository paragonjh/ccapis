# Crypto Currency APIs 
ccAPIs is a collection of API Clients for International Crypto Currency Exchanges.

It comes with two parts - `ccapis.apis` represents the base level API
interfaces, on top of which the second part - `ccapis.interfaces` - builds upon.
`ccapis.apis` classes can be used without making use of the interface classes.

Donations welcome!
BTC @ 3Fqm8RLGZduUkHrmRiNVE6794GumHthSq4

# State
--------------------------------

**RESTAPI** : **Completed**

**WSSAPI** : **BETA**

**Interfaces** : **WIP**

--------------------------------


# Supported Exchanges

| Exchange       | API  | Authentication | Public Endpoints*[^1] | Private Endpoints[^1] | Formatters | Tests |
|----------------|------|----------------|-------------------|--------------------|------------|-------|
| Bitfinex       | Done | Done           | Done              | Done               | WIP        | WIP   |
| Bitstamp       | Done | Done           | Done              | Done               | WIP        | WIP   |
| Bittrex        | Done | Done           | Done              | Done               | WIP        | WIP   |
| Bithumb        | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Coinone        | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Coinbase       | Done | BETA           | Done              | Done               | WIP        | WIP   |
| Upbit          | Done | BETA           | Done              | Done               | WIP        | WIP   |


Additional clients will be added to (or removed from) this list, 
according to their liquidity and market volume.

[^1]: This table considers standardized methods only, when describing the state. See section `Standardized Methods` for more

# ccapis.apis.REST

Classes found in `bitex.api.REST` provide wrapper classes and methods for Python's
`requests` module, including handling of each exchange's specific authentication
procedure.

An example:
```
from ccapis.apis.REST import BithumbREST

bt = BithumbREST()
bt.load_key('api.key')  # loads key and secret from given file;

# Query a public endpoint
bt.query('GET','public/Depth', params={'pair': 'XXBTZUSD'})

# Query a private (authenticated) endpoint
q = {'pair': 'XXBTZUSD', 'type': 'sell', 'ordertype': 'limit', 'price': 1000.0,
     'volume': 0.01, 'validate': True}
bt.query('POST','private/AddOrder', authenticate=True, params=q)

```

Example `.key` file:
```
>>>dummy.key
my_api_key
my_fancy_api_secret
```

If the api requires further details, for example a userid or account 
number (for example for bitstamp), you should check the class method's doc string,
although usually this information needs to go after the api key
and secret, on a separate line each.
```
>>>dummy2.key
my_api_key
my_fancy_api_secret
Userid
accountname
```

# ccapis.apis.WSS
`ccapis.apis.WSS` offers `Queue()`-based Websocket interface for a select few exchanges.
The classes found within are very basic, and subject to further development. Private
endpoints and trading are only sporadically implemented.

Their prime objective is to provide a raw, realtime interface to all of an exchange's
Websocket endpoint.

## Usage
```
from.ccapis.apis.WSS import BitfinexWSS
import time

wss = BitfinexWSS()
wss.start()
time.sleep(5)
wss.stop()

while not wss.data_q.empty():
    print(wss.data_q.get())
    
```
You can of course also access `data_q` while the `WebSocket` is still running 
(i.e. before calling `stop()`).

# ccapis.interfaces

Built on top of `ccapis.apis`'s api classes are the slightly more sophisticated
exchange interfaces in `bitex.interfaces`. These have been written to unify
the diverse REST APIs of the implemented exchanges, by providing the same methods and method parameters
across all of them (see next section, `Standardized Methods`, for more information).

For example, querying tickers looks the same on all exchanges, as well as
placing an order, using `bitex.interface`:

```
from ccapis import Bithumb, Bitfinex, Upbit
bt = Bithumb(key_file='bt.key')
bf = Bitfinex(key_file='bf.key')
ub = Upbit(key_file='ub.key')

bt.ticker('BTC', 'ETH')
bf.ticker('BTC', 'ETH')
ub.ticker('BTC', 'ETH')

bt.ask(base, counter, price, size)
bf.ask(base, counter, price, size)
ub.ask(base, counter, price, size)
```

# Standardized Methods

As explained in the previous section, __standardized methods__ refer to the methods of each interface
which have been deemed as part of the set of minimal methods and functions required to trade
at an exchange via its API. They feature the following characteristics:

- Each method has an identical method header across all interfaces
- Its output is identical across all interfaces
- Each method returns a `ccapis.apis.rest.RESTAPIResponse` object; these behave like `requests.Request` objects, with the addition
of a new attribute, `formatted`, which stores a standardized representation of the data queried.



# ccapis.formatters

This module provide formatters for the standardized methods, formatting their json output into a uniform layout. They are a work in progress feature.

Be mindful that, in order to provide a unified output format, some fields have been dropped in the formatted output! If you rely on one of these dropped fields, be sure to use the `RESTAPIResponse`'s `json` attribute instead, and parse the json yourself:

```
from bitex import Kraken
bf = Bitfinex()
response = bf.ticker()
print(response.formatted)  # show formatted data
print(response.json())  # Returns all json data
```

The following is a table of all formatters currently implemented - any method not marked as `Done` will not do any formatting.

| Exchange          | `ticker()` | order_book() | trades() | bid()/ask() | order() | cancel_order() | balance() | withdraw() | deposit() |
|-------------------|------------|--------------|----------|-------------|---------|----------------|-----------|------------|-----------|
| Bitfinex          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Bittrex           | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Poloniex          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Bithumb           | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Coinone           | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Coinbase          | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |
| Upbit             | Done       | Planned      | Planned  | Planned     | Planned | Planned        | Planned   | Planned    | Planned   |



# Installation

Manually, using the supplied `setup.py` file:

`python3 setup.py install`

or via pip

`pip install ccapis`

