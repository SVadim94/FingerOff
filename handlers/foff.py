from models import Chat, UserBalance
from utils.decorators import check_inited
from utils.dict_functions import (dict_equal_sums, dict_merge, dict_split,
                                  subset_sum)
from utils.strategies import run


@check_inited(True)
def foff(message):
    """/foff
    prints possible transactions"""
    transactions = []

    balances = { rec.user.username: rec.balance for rec in UserBalance.select().where(UserBalance.chat == Chat.get(id=message.chat.id)) }
    balances_pos, balances_neg = dict_split(balances)

    # eliminate equals
    while True:
        update = dict_equal_sums(balances, balances_pos, balances_neg)

        if not update:
            break

        transactions.extend(update)

    # eliminate sums
    if len(balances.keys()) < 20:
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
    to_str = lambda transactions: '\n'.join("/transfer %s %s %s" % (s, d, str(a)) for s, d, a in transactions)
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
