from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime
from .config import APP_KEY, ACCESS_KEY, SECRET_KEY
from pymesomb.exceptions import PermissionDeniedException

operation = PaymentOperation(APP_KEY, ACCESS_KEY, SECRET_KEY)


def collect_money(numero, montant, service="MTN", trx_id=None):
    """Recevoir de l'argent d'un client"""
    if trx_id is None:
        trx_id = RandomGenerator.nonce()

    try:
        result = operation.make_collect(
            amount=montant,
            service=service,
            payer=numero,
            nonce=RandomGenerator.nonce(),
        )
        return {"success": True, "data": result}

    except PermissionDeniedException as e:
    # Cas où l'utilisateur n'est pas activé

        return {"success": False, "error": str(e)}


def deposit_money(numero, montant, service="MTN", trx_id=None):
    """Envoyer de l'argent à un client"""
    if trx_id is None:
        trx_id = RandomGenerator.nonce()

    return operation.make_deposit(
        amount=montant,
        service=service,
        receiver=numero,
        nonce=RandomGenerator.nonce()
    )
'''
from pymesomb.operations import PaymentOperation
import requests
data2 = client.make_collect(amount=100, service='MTN', payer='670000000', trx_id='1', customer={
    'phone': '+237658308288',
    'email': 'kiaranarol@gmail.com',
    'first_name': 'Arol',
    'last_name': 'Kieran',
}, location={
    'town': 'Douala',
    'region': 'Littoral',
    'country': 'Cameroun'
}, products=[

])
data2.is_operation_success()
data2.is_transaction_success()
url="/api/v1.1/payment/collect"
response= requests.post(url,json=data2)
'''