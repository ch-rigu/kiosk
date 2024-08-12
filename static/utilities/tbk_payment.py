
import uuid
from transbank.webpay.webpay_plus.transaction import *
from transbank.error.transaction_create_error import TransactionCreateError
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
import random
import string
import datetime

api_key = "ec294819-3d94-4f37-aa1e-1f61cc66f941"
commerce_code = "597048378510"

def random_string():
    fecha_actual = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    caracteres = string.ascii_letters + string.digits
    longitud_maxima = 26 - len(fecha_actual)
    cadena_random = ''.join(random.choice(caracteres) for _ in range(longitud_maxima))
    return fecha_actual + cadena_random


def start_transaction(amount, buy_order, session_id, return_url, production):
    if production:
        tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))
    else:
         tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    
    resp = tx.create(buy_order, session_id, amount, return_url)
    return resp

def commit_transaction(token, production):
    if production:
        tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))
    else:
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.commit(token)
    print(resp)

    return resp

def refund_transaction(token, amount, production):
    if production:
        tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))
    else:
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.refund(token, amount)
    print(resp)

    return resp

def status_transaction(token, production):
    if production:
        tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))
    else:
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.status(token)
    print(resp)

    return resp

def capture_transaction(token, buy_order, authorization_code, capture_amount, production):
    if production:
        tx = Transaction(WebpayOptions(commerce_code, api_key, IntegrationType.LIVE))
    else:
        tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))
    resp = tx.capture(token, buy_order, authorization_code, capture_amount)
    print(resp)

    return resp