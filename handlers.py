from forex_python.converter import CurrencyRates, CurrencyCodes
from models import Debt, User, Chat
from decimal import Decimal
import config


cc = CurrencyCodes()
cr = CurrencyRates()


def check_currency(currency, default_currency):
    currency = currency.upper()

    if cc.get_currency_name(currency):
        return currency
    else:
        return default_currency


def add(chat_id, src, dst, amount, currency=None):
    chat, _ = Chat.get_or_create(chat_id=chat_id)
    src, _ = User.get_or_create(username=src)
    dst, _ = User.get_or_create(username=dst)
    amount = Decimal(amount)

    currency = check_currency(currency, chat.currency)

    if currency != chat.currency:
        amount = cr.convert(currency, chat.currency, amount)

    debt = Debt(src=src, dst=dst, amount=amount)
    debt.save()

    return '%s -> %s: %d' % (src.username, dst.username, amount)


def set_default_currency(chat_id, currency):
    chat, _ = Chat.get_or_create(chat_id=chat_id)
    old_currency = chat.currency
    chat.currency = check_currency(currency, chat.currency)
    chat.save()

    return "Changed the default currency from %s to %s" % (old_currency, chat.currency)


def usage(_):
    return """\
Usage:

/add <src> <dst> <amount> [currency] - add a debt
/set_default_currency <currency> - set default currency for debts
/optimize [name] ... - optimizes number of transactions between 
/usage - show this message
"""


def evaler(args):
    return eval(' '.join(args))

cb = {
    "/add": add,
    "/eval": evaler,
    "/set_default_currency": set_default_currency,
    "/usage": usage
}

