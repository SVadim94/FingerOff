from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from models import Chat, Transaction, TransactionType
from utils.currency import check_currency, convert
from utils.db import get_or_create_user, merge_transaction
from utils.decorators import check_inited


@check_inited(True)
def transfer(message, creditor, debtor, amount, currency=None):
    """/transfer <debtor> <creditor> <amount> [currency]
    transfer a debt"""
    chat, _ = Chat.get_or_create(id=message.chat.id)
    creditor = get_or_create_user(creditor)
    debtor = get_or_create_user(debtor)
    amount = Decimal(amount)
    original_amount = amount

    currency = check_currency(currency, chat.currency)

    if currency is None:
        return available_currencies()

    if currency != chat.currency:
        amount = convert(currency, chat.currency, amount)

    transaction = Transaction(
        chat=chat,
        transaction_id=uuid4(),
        transaction_type=TransactionType.DEBT.value,
        timestamp=datetime.now(),
        debtor=debtor,
        creditor=creditor,
        amount=amount,
        currency=chat.currency,
        original_amount=original_amount,
        original_currency=currency
    )
    transaction.save()

    merge_transaction(transaction)

    return str(transaction)
