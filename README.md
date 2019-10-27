# unnamed-exchange-python
Python3 bindings for unnamed.exchange

https://www.digitalmoneybits.org/

https://github.com/digitalmoneybits2/unnamed-exchange-python


API Documentation
-------------

[Official API Documentation](https://www.unnamed.exchange/Home/Api)



Example Usage for Unnamed.exchange API
-------------
first edit the lines:

```python3
api_key = "<my_api_key>"

api_secret = "<my_api_secret>"
```

  with your api key and secret

get your API key here:
https://www.unnamed.exchange/UserSettings


```python3
#!/usr/bin/python3
import UnnamedAPI


api_key = "<my_api_key>"
api_secret = "<my_api_secret>"


# https://github.com/digitalmoneybits2/unnamed-exchange-python
# https://www.digitalmoneybits.org/

API = UnnamedAPI.UnnamedAPI(api_key, api_secret)

# # PublicAPI
# print(API.get_ping())
# print(API.get_time())
print(API.get_markets())
# print(API.get_currencies())
print(API.get_ticker('DMB_BTC'))
# print(API.get_24h_sum('DMB_BTC'))
# print(API.get_order_book('DMB_BTC'))
# print(API.get_history('DMB_BTC'))

# # PrivateAPI
# print(API.get_open_orders())
# print(API.get_open_orders('DMB_BTC'))
print(API.get_trades())
# print(API.get_trades('DMB_BTC'))
# print(API.get_balance())
# print(API.get_balance('DMB'))
# print(API.get_balance_full())
# print(API.get_balance_full('DMB'))
# print(API.get_closed_orders())
# print(API.get_closed_orders('DMB_DOGE'))
# print(API.sell_limit('DMB_BTC', 300.00000000, 0.00000200))
# print(API.cancel(123456))
# print(API.cancel_market('LTC_BTC'))
```
