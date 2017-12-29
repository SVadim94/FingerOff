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