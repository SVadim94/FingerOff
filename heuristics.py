def self_debt(opt_debts):
    for debt in opt_debts:
        if debt.amount == 0:
            debt.delete_instance()


def transitive(opt_debts):
    passed = []

    for elem in opt_debts:
        for second in passed:
            # DO STUFF
            passed.append(elem)


def rucksack(opt_debts):
    pass

heuristics = [
    self_debt,
    rucksack
]
