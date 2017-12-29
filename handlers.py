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
    transactions = []

    balances = { rec.user.username: rec.balance for rec in UserBalance.select() }
    balances_pos, balances_neg = dict_split(balances)

    # eliminate equals
    while True:
        update = dict_equal_sums(balances, balances_pos, balances_neg)

        if not update:
            break

        transactions.extend(update)

    # eliminate sums
    to_del = []

    for kn, vn in balances_neg.items():
        group = subset_sum(balances_pos, -vn)

        if group:
            for kp in group:
                # add transaction
                transactions.append((kp, kn, balances_pos[kp]))

                # update balances
                dict_merge(balances, (kp, kn, balances_pos[kp]))

                # update balances_pos
                del balances_pos[kp]

            to_del.append(kn)

    for kn in to_del:
        del balances_neg[kn]

    text = ""
    cur_code = Chat.get(Chat.id == message.chat.id).currency
    to_str = lambda transactions: '\n'.join("/add %s %s %s" % (s, d, str(a)) for s, d, a in transactions)
    easy_part = to_str(transactions)
    if easy_part:
        text += \
"""Easy part is:

%s

""" % easy_part

    if balances:
        result, desc_debtor, desc_creditor, desc_amount = min(run(balances), key=lambda x: x[3])
        hard_part = \
"""Strategy: the debtor %(desc_debtor)s debt transfers the %(desc_amount)s to the creditor %(desc_creditor)s credit
Total transfers: %(total)d

%(result)s
""" % {
    "desc_debtor": desc_debtor,
    "desc_creditor": desc_creditor,
    "desc_amount": desc_amount,
    "total": len(result),
    "result": to_str(result)
}
        text += \
"""The hard part is the following:
%s
""" % hard_part

    return text

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
