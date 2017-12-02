from interfaces import Bittrex
from ccapis.apis.REST import BittrexREST

# from ccapis import Bithumb
# from ccapis.apis.REST import BithumbREST


print("=============================")
bittrex = Bittrex()
# bittrex.load_key('Bittrex.key')

response = bittrex.ticker("BTC","ETH")
print()
print("===== Bittrex ticker1 ======")
# print(response.json())
print("===== Bittrex ticker2 ======")
print(response.formatted)


# response = k.balance()
# print()
# print("===== balance ======")
# print(response.json())
#
# response = k.order_book('BTC-ETH')
# print()
# print("===== order book1 ======")
# print(response.formatted)
# print("===== order book2 ======")
# print(response.json())
# print(response.formatted)
#
#
# from ccapis.apis.rest import RESTAPIClient
#
# # bithumb = Bithumb()
# # bithumb.load_key('bithumb.key')
# #
# # response = bithumb.ticker('BTC')
# # print("===== Bithumb ticker1 ======")
# # print(response.json())
# # print("===== Bithumb ticker2 ======")
# # print(response.formatted)
# # print("=============================")
# # response = bithumb.order_book('BTC',count=20)
# # print("===== Bithumb orderBook1 ======")
# # print(response.json())
# # print("===== Bithumb orderBook2 ======")
# # print(response.formatted)
# # print("=============================")
#








