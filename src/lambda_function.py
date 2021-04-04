import math
import os
from decimal import Decimal

from bitflyer.api import BitflyerAPI, SendNewOrderRequestBody


def lambda_handler(event, context):
    api_key = os.environ["key"]
    api_secret = os.environ["secret"]

    child_order_type = "MARKET"  # only handle market order case
    side = "BUY"  # only BUY and HODL!
    price = 0  # hardcode to 0 for market order

    product_code = os.environ["product"]  # 'ETH_JPY or 'BTC_JPY'
    target_cost = int(os.environ["target_cost"])

    bitflyer = BitflyerAPI(api_key, api_secret)

    # Bitflyer only allow to send size of ETH with unit of 6 and BTC of 7
    # Use 6 for convinience to round up
    size_precision = 6

    ticker_resp = bitflyer.get_ticker(product_code)
    ticker = ticker_resp.json()

    last_tick_price = ticker["ltp"]  # last tick price
    size = float(Decimal(target_cost) / Decimal(last_tick_price))
    precision_adjusted_size = float(
        Decimal(math.floor(size * 10 ** size_precision)) / Decimal(10 ** size_precision)
    )

    send_order_request = SendNewOrderRequestBody(
        product_code, child_order_type, side, price, precision_adjusted_size
    )
    resp = bitflyer.send_new_order(send_order_request)
    return {
        "statusCode": resp.status_code,
        "headers": {"Content-Type": "application/json"},
        "data": resp.json(),
    }
