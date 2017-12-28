from forex_python.converter import CurrencyCodes, CurrencyRates

import config
from models import Chat, User, UserBalance, db

cc = CurrencyCodes()
cr = CurrencyRates(force_decimal=True)


def check_inited(need_to_be_inited, need_to_be_checked=True):
    def wrapper(foo):
        if not need_to_be_checked:
            return foo

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


def is_int(n):
    try:
        int(n, 10)
        return True
    except ValueError:
        return False


def join_columns(columns):
    res = "\n".join(str(_) for _ in columns)

    return res if res else "No results"


def merge_transaction(transaction):
    with db.atomic():
        creditor, _ = UserBalance.get_or_create(chat=transaction.chat, user=transaction.creditor)
        creditor.balance -= transaction.amount

        if creditor.balance == 0:
            creditor.delete_instance()
        else:
            creditor.save()

        debtor, _ = UserBalance.get_or_create(chat=transaction.chat, user=transaction.debtor)
        debtor.balance += transaction.amount

        if debtor.balance == 0:
            debtor.delete_instance()
        else:
            debtor.save()


def get_or_create_user(username):
    return User.get_or_create(username=username.lower())[0]

def subset_sum(users, ss=0):
    sums = {}

    for (user, balance) in users.items():
        tmp = sums.copy()

        tmp[balance] = (user,)

        for (cur_sum, cur_users) in sums.items():
            if (cur_sum + balance) not in tmp:
                tmp[cur_sum + balance] = cur_users + (user,)

        sums = tmp

        if ss in sums:
            return sums[ss]
