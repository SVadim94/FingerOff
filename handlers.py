from datetime import datetime
from decimal import Decimal
from itertools import filterfalse
from uuid import uuid4

from models import Chat, Transaction, TransactionType, User, UserBalance
from utils import *


@check_inited(True)
def add(message, creditor, debtor, amount, currency=None):
    chat, _ = Chat.get_or_create(id=message.chat.id)
    creditor = get_or_create_user(creditor)
    debtor = get_or_create_user(debtor)
    amount = Decimal(amount)
    original_amount = amount

    currency = check_currency(currency, chat.currency)

    if currency != chat.currency:
        amount = cr.convert(currency, chat.currency, amount)

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


@check_inited(False)
def set_default_currency(message, currency='RUB'):
    chat, _ = Chat.get_or_create(id=message.chat.id)
    old_currency = chat.currency
    chat.currency = check_currency(currency, chat.currency)
    chat.inited = True
    chat.save()

    return "Changed the default currency from %s to %s" % (old_currency, chat.currency)


@check_inited(True)
def balance(message):
    return join_columns(UserBalance.select().where(UserBalance.chat == Chat.get(Chat.id == message.chat.id)))


@check_inited(True)
def show(message, *args):
    usernames = [_ for _ in args if _.startswith('@')]
    numbers = [_ for _ in args if is_int(_)]

    query = Chat.id == message.chat.id

    if usernames:
        for username in usernames:
            username = username.lower()

            try:
                user = User.get(User.username == username)
            except:
                return "No such user %s" % username

            query &= (Transaction.creditor == user) | (Transaction.debtor == user)

    if numbers:
        N = int(numbers[0])
    else:
        N = 10

    return join_columns(Transaction.select().join(Chat).where(query).order_by(Transaction.timestamp.desc()).limit(N))


@check_inited(True)
def foff(message):
    return "Not implemented"

@check_inited(False, False)
def usage(_):
    return """\
Usage:

/init <currency>
    set default currency for debts (default is RUB)
/add <debtor> <creditor> <amount> [currency]
    add a debt
/balance
    shows balance for current chat
/foff
    prints possible transactions
/show [N] [@nickname] [@nickname]
    prints transactions:
        N - last N transactions (default 10)
        @nickname - transactions related to @nickname user
/cancel <transaction_id>
    cancels transaction by its id
/archive
    archives debts history and returns archive's id
/get <archive_id>
    get archive by id
/purge
    cleans debts history (history will be archived)
/usage
    show this message
"""


handlers = {
    "/init": set_default_currency,
    "/add": add,
    "/balance": balance,
    "/foff": foff,
    "/show": show,
    "/usage": usage
}
