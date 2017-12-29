from .decorators import add_desc
from .dict_functions import dict_merge, dict_split


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
