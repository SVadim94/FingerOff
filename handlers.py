from datetime import date, datetime, timedelta
from decimal import Decimal
from itertools import filterfalse
from uuid import uuid4

from forex_python.converter import CurrencyCodes, CurrencyRates

from models import Chat, DebtGraph, Transaction, TransactionType, User
from utils import is_int, join_columns

cc = CurrencyCodes()
cr = CurrencyRates()


def check_inited(need_to_be_inited):
    def wrapper(foo):
        def wrapped(*args, **kwargs):
            chat, _ = Chat.get_or_create(id=args[0].chat.id)

            if need_to_be_inited == chat.inited:
                return foo(*args, **kwargs)

            if need_to_be_inited:
                return "Please, /init first"
            else:
                return "Already inited"

        return wrapped

    return wrapper


def check_currency(currency, default_currency):
    if not currency:
        return default_currency

    currency = currency.upper()

    if cc.get_currency_name(currency):
        return currency
    else:
        return default_currency


@check_inited(True)
def add(message, creditor, debtor, amount, currency=None):
    chat, _ = Chat.get_or_create(id=message.chat.id)
    creditor, _ = User.get_or_create(username=creditor.upper())
    debtor, _ = User.get_or_create(username=debtor.upper())
    amount = Decimal(amount)
    original_amount = amount

    currency = check_currency(currency, chat.currency)

    if currency != chat.currency:
        amount = cr.convert(currency, chat.currency, amount)
    transaction = Transaction(
        chat=chat,
        transaction_id=uuid4(),
        transaction_type=TransactionType.DEBT.value,
        date=datetime.now(),
        debtor=debtor,
        creditor=creditor,
        amount=amount,
        currency=chat.currency,
        original_amount=original_amount,
        original_currency=currency
    )
    transaction.save()

    debt_graph = DebtGraph.load_graph(chat)
    debt_graph.add_debt(transaction)
    DebtGraph.save_graph(chat, debt_graph)

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
def show(message, *args):
    if args[0] == "all":
        return join_columns(Transaction.select())

    usernames = [ _ for _ in args if _.startswith('@')]
    numbers = [_ for _ in args if is_int(_)]

    if not numbers and not usernames:
        return "See /usage for the help"

    query = Chat.id == message.chat.id
    if usernames:
        username = usernames[0].upper()

        try:
            user = User.get(User.username == username)
        except:
            return "No such user %s" % username

        query &= (Transaction.creditor == user) | (Transaction.debtor == user)

    if numbers:
        N = int(numbers[0])
        last_N = Transaction.date >= (date.today() - timedelta(days=N))
        query &= last_N

    return join_columns(Transaction.select().join(Chat).where(query))


def usage(_):
    return """\
Usage:

/init <currency> - set default currency for debts
/add <src> <dst> <amount> [currency] - add a debt
/show all
    prints all transactions
/show [N] [@nickname]
    prints all transactions:
        N - in N days
        @nickname - related to @nickname user
/usage - show this message
"""


handlers = {
    "/init": set_default_currency,
    "/add": add,
    "/show": show,
    "/usage": usage
}
