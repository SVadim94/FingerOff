from forex_python.converter import CurrencyRates, CurrencyCodes
from models import Debt, User, Chat, DebtGraph
from decimal import Decimal


cc = CurrencyCodes()
cr = CurrencyRates()


def check_currency(currency, default_currency):
    if not currency:
        return default_currency

    currency = currency.upper()

    if cc.get_currency_name(currency):
        return currency
    else:
        return default_currency


def add(message, lender, debtor, amount, currency=None):
    chat, _ = Chat.get_or_create(id=message.chat.id)
    lender, _ = User.get_or_create(username=lender[1:].upper())
    debtor, _ = User.get_or_create(username=debtor[1:].upper())
    amount = Decimal(amount)

    currency = check_currency(currency, chat.currency)

    if currency != chat.currency:
        amount = cr.convert(currency, chat.currency, amount)

    debt = Debt(chat=chat, lender=lender, debtor=debtor, amount=amount)
    debt.save()

    DebtGraph.add(debt)

    return str(debt)


def set_default_currency(message, currency):
    chat, _ = Chat.get_or_create(id=message.chat.id)
    old_currency = chat.currency
    chat.currency = check_currency(currency, chat.currency)
    chat.save()

    return "Changed the default currency from %s to %s" % (old_currency, chat.currency)


def optimize(message):
    sender = message.from_user.username

    loans = [Debt.select().where(User.lender == sender)]
    debts = [Debt.select().where(User.debtor == sender)]

    return message.from_user.username


def usage(_):
    return """\
Usage:

/add <src> <dst> <amount> [currency] - add a debt
/set_default_currency <currency> - set default currency for debts
/optimize [name] ... - optimizes number of transactions between 
/usage - show this message
"""


handlers = {
    "/add": add,
    "/set_default_currency": set_default_currency,
    "/optimize": optimize,
    "/usage": usage
}
