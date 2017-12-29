from forex_python.converter import CurrencyCodes, CurrencyRates

import config
from models import Chat, User, UserBalance, db

cc = CurrencyCodes()
cr = CurrencyRates(force_decimal=True)


def check_inited(need_to_be_inited, need_to_be_checked=True):
    def wrapper(foo):
        def wrapped(*args, **kwargs):
            if not need_to_be_checked:
                return foo(*args, **kwargs)

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


def dict_split(dic):
    dic_pos = { k: v for k, v in dic.items() if v > 0 }
    dic_neg = { k: v for k, v in dic.items() if v < 0 }

    return (dic_pos, dic_neg)


def dict_equal_sums(balances, balances_pos, balances_neg):
    transactions = []

    rev_balances_pos = { v: k for k, v in balances_pos.items() }
    rev_balances_neg = { v: k for k, v in balances_neg.items() }

    for vp, kp in rev_balances_pos.items():
        for vn, kn in rev_balances_neg.items():
            if vp + vn == 0:
                # add transaction
                transactions.append((kp, kn, vp))

                # update balances
                dict_merge(balances, (kp, kn, vp))

                # update balances_pos and balances_neg
                del balances_pos[kp]
                del balances_neg[kn]

    return transactions


def dict_merge(dic, transaction):
    x, y, a = transaction

    assert x in dic
    assert y in dic

    dic[x] -= a
    dic[y] += a

    if dic[x] == 0:
        del dic[x]

    if dic[y] == 0:
        del dic[y]


def add_desc(desc):
    def wrapper(foo):
        foo.desc = desc
        return foo

    return wrapper


@add_desc("with a maximum")
def get_max(dic):
    k = max(dic, key=lambda x: dic[x])

    return k, dic[k]


@add_desc("with a minimum")
def get_min(dic):
    k = min(dic, key=lambda x: dic[x])

    return k, dic[k]


@add_desc("amount that is less or equal to the value creditor is able to receive")
def not_more(debtor, creditor):
    kd, vd = debtor
    kc, vc = creditor

    return min(vd, -vc)


@add_desc("amount that is equals to the overall debtor's debt")
def all_money(debtor, creditor):
    return debtor[1]


def run(balances):
    for get_debtor in [get_max, get_min]:
        for get_creditor in [get_max, get_min]:
            for get_amount in [not_more]:#, all_money]:
                yield (
                    run_strategy(balances.copy(), get_debtor, get_creditor, get_amount),
                    get_debtor.desc,
                    get_creditor.desc,
                    get_amount.desc
                )

def run_strategy(balances, get_debtor, get_creditor, get_amount):
    transactions = []

    while balances:
        balances_pos, balances_neg = dict_split(balances)
        debtor = get_debtor(balances_pos)
        creditor = get_creditor(balances_neg)
        amount = get_amount(debtor, creditor)
        transaction = (debtor[0], creditor[0], amount)
        transactions.append(transaction)
        dict_merge(balances, transaction)

    return transactions
