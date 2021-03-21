import os

from bitflyer.api import BitflyerAPI, SendNewOrderRequestBody


def lambda_handler(event, context):
    api_key = os.environ["key"]
    api_secret = os.environ["secret"]
    product_code = os.environ["product"]
    child_order_type = os.environ["order_type"]  # 'LIMIT' or 'MARKET'
    side = os.environ["side"]  # 'BUY' or 'SELL'
    try:
        price = int(os.environ["price"])
        size = float(os.environ["size"])
    except ValueError:
        return get_bad_request(400)

    bitflyer = BitflyerAPI(api_key, api_secret)
    send_order_request = SendNewOrderRequestBody(
        product_code, child_order_type, side, price, size
    )

    try:
        bitflyer.send_new_order(send_order_request)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
        }
    except RuntimeError:
        return get_bad_request(500)


def get_bad_request(status_code: int):
    return {"statusCode": status_code}
