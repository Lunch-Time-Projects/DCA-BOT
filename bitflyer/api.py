import json
import hmac
import hashlib
import requests
import time
from datetime import datetime
from dataclasses import dataclass

class BitflyerAPI:
    """
    This is the API wrapper for calling bitflyer lightening.
    See the doc: https://lightning.bitflyer.com/docs
    """

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.bitflyer.com'

    def get_ticker(self, product_code: str):
        resp = requests.get(
            self.base_url + '/v1/ticker?product_code={}'.format(product_code),
        )
        return resp

    def get_balance(self):
        timestamp = str(time.time())
        method = 'GET'
        path = '/v1/me/getbalance'

        return requests.get(
            self.base_url + path,
            headers=self._get_headers(timestamp, method, path)
        )

    def get_orders(self, query: 'GetOrdersQuery'):
        timestamp = str(time.time())
        method = 'GET'
        path = '/v1/me/getchildorders' + query.encoded

        return requests.get(
            self.base_url + path,
            headers=self._get_headers(timestamp, method, path)
        )

    def send_new_order(self, body: 'SendNewOrderRequestBody'):
        timestamp = str(time.time())
        method = 'POST'
        path = '/v1/me/sendchildorder'

        body = json.dumps(body.__dict__, separators=(',', ':'))

        return requests.post(
            self.base_url + path,
            headers=self._get_headers(timestamp, method, path, body),
            data=body
        )


    def _build_signature(self, timestamp, method, path, body=''):
        text = timestamp + method + path + body
        return hmac.new(
            self.api_secret.encode('utf-8'),
            msg=text.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest().lower()


    def _get_headers(self, timestamp, method, path, body=''):
        sign = self._build_signature(timestamp, method, path, body)
        return {
            'ACCESS-KEY': self.api_key,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': sign,
            'Content-Type': 'application/json'
        }

@dataclass
class SendNewOrderRequestBody:
    product_code: str
    child_order_type: str # 'LIMIT' or 'MARKET'
    side: str # 'BUY' or 'SELL'
    price: int
    size: float

    # default to 5 minutes
    minute_to_expire: int = 5

    # default to 'GTC' (good til cancelled), other options are:
    # 'IOC' (Immediate or Cancel) and 'FOK' (fill or kill)
    time_in_force: str = 'GTC'

@dataclass
class GetOrdersQuery:
    product_code: str  # 'BTC_JPY' or 'ETH_JPY
    child_order_acceptance_id: str = ''

    @property
    def encoded(self):
        result = '?product_code={}'.format(self.product_code)

        if self.child_order_acceptance_id != '':
            result += '&child_order_acceptance_id={}'.format(self.child_order_acceptance_id)

        return result

