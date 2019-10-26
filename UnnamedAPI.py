from time import time
import hmac
import hashlib
import requests
from retrying import retry

# https://github.com/digitalmoneybits2/unnamed-exchange-python
# https://www.digitalmoneybits.org/


class UnnamedX(object):
    def __init__(self):
        self.BASE_URL = 'https://api.unnamed.exchange/v1/'

    @retry(stop_max_attempt_number=3)
    def get_data(self, urldir, params=''):
        params += 'nonce=' + self.get_nonce()
        reqUrl = self.BASE_URL + urldir + '?' + params
        r = requests.get(reqUrl).json()
        return r if r else None

    @retry(stop_max_attempt_number=3)
    def post_data(self, urldir, params=''):
        params += 'nonce=' + self.get_nonce()
        reqUrl = self.BASE_URL + urldir + '?' + params
        Sign = self.hmac_sign(params, self._secret)
        headers = {'apikey': self._api_key, 'signature': Sign}
        r = requests.post(reqUrl, data=params, headers=headers)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise Exception("bad response")

    @staticmethod
    def get_nonce():
        return str(int(time() * 1000))

    @staticmethod
    def hmac_sign(msg_str, secret_bytes):
        return hmac.new(secret_bytes, msg_str.encode('utf-8'),
                        hashlib.sha512).hexdigest()


class UnnamedAPI(UnnamedX):
    def __init__(self, api_key=None, api_secret=None):
        UnnamedX.__init__(self)
        self._api_key = api_key
        self._secret = api_secret.encode() if api_secret else None

    # PublicAPI
    def get_ping(self):  # {"result": "Pong"}
        return self.get_data('Public/Ping')

    def get_time(self):
        return self.get_data('Public/Time')

    def get_markets(self):
        return self.get_data('Public/MarketInfo')

    def get_currencies(self):
        return self.get_data('Public/AssetInfo')

    def get_ticker(self, market):
        params = 'market={}&'.format(market)
        return self.get_data('Public/Ticker', params)

    def get_24h_sum(self, market):
        params = 'market={}&'.format(market)
        return self.get_data('Public/Chart', params)

    def get_order_book(self, market):
        params = 'market={}&'.format(market)
        return self.get_data('Public/OrderBook', params)

    def get_history(self, market):
        params = 'market={}&'.format(market)
        return self.get_data('Public/TradeHistory', params)

    # PrivateAPI
    @staticmethod
    def _format_params(market='', count=0, coinsymbol=''):
        params = ''
        if market:
            params += 'market={}&'.format(market)
        elif coinsymbol:
            params += 'symbol={}&'.format(coinsymbol)
        if count > 0:
            params += 'count={:d}&'.format(count)
        return params

    def get_open_orders(self, market=''):
        urlpath = 'Trade/Orders'
        params = self._format_params(market=market)
        return self.post_data(urlpath, params)

    def get_closed_orders(self, market='', count=0):
        urlpath = 'Trade/OrderHistory'
        params = self._format_params(market=market, count=count)
        return self.post_data(urlpath, params)

    def get_trades(self, market='', count=0):
        urlpath = 'Trade/TradeHistory'
        params = self._format_params(market=market, count=count)
        return self.post_data(urlpath, params)

    def get_balance(self, coinsymbol=''):
        urlpath = 'Trade/Balance'
        params = self._format_params(coinsymbol=coinsymbol)
        return self.post_data(urlpath, params)

    def get_balance_full(self, coinsymbol=''):
        urlpath = 'Trade/BalanceFull'
        params = self._format_params(coinsymbol=coinsymbol)
        return self.post_data(urlpath, params)

    def _order(self, M, otype, quantity, rate=None, ocon='Limit', stop=None):
        # otype: Buy / Sell
        # ocon: Limit / Market / StopLimit
        params = 'market={}&orderType={}&type={}&amount={:.8f}&'
        params = params.format(M, ocon, otype, quantity)
        if rate:
            params += 'price={:.8f}&'.format(rate)
        if stop:
            params += 'stop={:.8f}&'.format(stop)
        return self.post_data('Trade/OrderSubmit', params)

    def buy_limit(self, market, quantity, rate):
        return self._order(market, 'Buy', quantity, rate)

    def sell_limit(self, market, quantity, rate):
        return self._order(market, 'Sell', quantity, rate)

    def buy_market(self, market, quantity):
        return self._order(market, 'Buy', quantity, ocon='Market')

    def sell_market(self, market, quantity):
        return self._order(market, 'Sell', quantity, ocon='Market')

    def cancel(self, uuid):
        params = 'cancelType=Trade&orderType=Limit&orderId={}&'.format(uuid)
        return self.post_data('Trade/OrderCancel', params)

    def cancel_market(self, M):
        params = 'market={}&cancelType=TradePair&orderType=Limit&'.format(M)
        return self.post_data('Trade/OrderCancel', params)
