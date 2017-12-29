import unittest
from random import choice, choices, randrange

from models import User, UserBalance
from tutils import *
from utils import *


class TestUtils(unittest.TestCase):
    def test_is_int(self):
        self.assertTrue(is_int('0'))
        self.assertTrue(is_int('-1337'))
        self.assertTrue(is_int('1337'))

        self.assertFalse(is_int('0x0'))
        self.assertFalse(is_int('Some text'))
        self.assertFalse(is_int('123a'))
        self.assertFalse(is_int('1e1'))

    def test_join_columns(self):
        self.assertEqual(join_columns([1,2,3]), "1\n2\n3")
        self.assertEqual(join_columns(['a']), "a")

        self.assertEqual(join_columns([]), 'No results')

    def test_merge_transactions(self):
        self.chat = create_chat()

        t1 = make_transaction_mock(
            chat=self.chat,
            debtor=get_or_create_user(test_users[0]),
            creditor=get_or_create_user(test_users[1]),
            amount=1
        )

        t2 = make_transaction_mock(
            chat=self.chat,
            debtor=get_or_create_user(test_users[1]),
            creditor=get_or_create_user(test_users[2]),
            amount=2
        )

        t3 = make_transaction_mock(
            chat=self.chat,
            debtor=get_or_create_user(test_users[2]),
            creditor=get_or_create_user(test_users[0]),
            amount=1
        )

        merge_transaction(t1)

        check = lambda name, balance: self.assertEqual(
            UserBalance.get(
                (UserBalance.chat == self.chat) &
                (UserBalance.user == get_or_create_user(name))
            ).balance,
            balance
        )

        check(test_users[0], 1)
        check(test_users[1], -1)
        with self.assertRaises(peewee.DoesNotExist):
            check(test_users[2], 0)

        merge_transaction(t2)

        check(test_users[0], 1)
        check(test_users[1], 1)
        check(test_users[2], -2)

        merge_transaction(t3)

        with self.assertRaises(peewee.DoesNotExist):
            check(test_users[0], 0)
        check(test_users[1], 1)
        check(test_users[2], -1)

        destroy_chat()

    def test_get_or_create_user(self):
        for _ in range(2):
            for username in test_users:
                user = get_or_create_user(username)
                self.assertEqual(user.username, username.lower())
                user.delete_instance()

    def test_dict_split(self):
        for _ in range(100):
            dic = generate_test_set(valid=True)
            dic_pos, dic_neg = dict_split(dic)
            sp, sn, s = set(dic_pos.keys()), set(dic_neg.keys()), set(dic.keys())

            self.assertDictContainsSubset(dic_pos, dic)
            self.assertDictContainsSubset(dic_neg, dic)
            self.assertSetEqual(sp | sn, s)
            self.assertSetEqual(sp & sn, set())

    def test_dict_equal_sums(self):
        for _ in range(100):
            dic, _ = generate_test_set(valid=False)
            dic[test_users[0]] = randrange(-2**32, 2**32)
            dic[test_users[1]] = -dic[test_users[0]]
            dic_pos, dic_neg = dict_split(dic)

            if not dic_pos or not dic_neg:
                continue

            cdic = dic.copy()
            cdic_pos = dic_pos.copy()
            cdic_neg = dic_neg.copy()

            self.assertTrue(dict_equal_sums(dic, dic_pos, dic_neg))
            self.assertNotEqual(cdic, dic)
            self.assertNotEqual(cdic_pos, dic_pos)
            self.assertNotEqual(cdic_neg, dic_neg)

            cdic = dic.copy()
            cdic_pos = dic_pos.copy()
            cdic_neg = dic_neg.copy()

            self.assertFalse(dict_equal_sums(dic, dic_pos, dic_neg))
            self.assertDictEqual(cdic, dic)
            self.assertDictEqual(cdic_pos, dic_pos)
            self.assertDictEqual(cdic_neg, dic_neg)

    def test_subset_sum(self):
        for _ in range(100):
            balances, ss = generate_test_set(valid=False)
            group = subset_sum(balances, ss)
            self.assertEqual(sum(balances[user] for user in group), ss)

    def test_dict_merge(self):
        ranges = (1, 2**32), (-2**32, -1)

        for i in range(100):
            balances = generate_test_set(valid=True)
            x, y = choices([key for key in balances.keys()], k=2)

            old_x_balance, old_y_balance = balances[x], balances[y]
            dict_merge(balances, (x, y, randrange(*ranges[i % 2])))

            if x != y:
                self.assertNotEqual(balances[x], old_x_balance)
                self.assertNotEqual(balances[y], old_y_balance)

            self.assertEqual(balances[x] + balances[y], old_x_balance + old_y_balance)
            self.assertEqual(sum(balances.values()), 0)
    
    def test_get_max(self):
        for _ in range(10):
            balances = generate_test_set(valid=True)
            k, v = get_max(balances)
            self.assertIn(k, balances)
            self.assertEqual(v, balances[k])
            self.assertEqual(v, max(balances.values()))
    
    def test_get_min(self):
        for _ in range(10):
            balances = generate_test_set(valid=True)
            k, v = get_min(balances)
            self.assertIn(k, balances)
            self.assertEqual(v, balances[k])
            self.assertEqual(v, min(balances.values()))

    def test_not_more(self):
        for _ in range(10):
            balances = generate_test_set(valid=True)
            balances_pos, balances_neg = dict_split(balances)
            debtor = choice(list(balances_pos.items()))
            creditor = choice(list(balances_neg.items()))
            amount = not_more(debtor, creditor)
            self.assertLessEqual(amount, debtor[1])
            self.assertLessEqual(amount, -creditor[1])

    def test_all_money(self):
        for _ in range(10):
            balances = generate_test_set(valid=True)
            balances_pos, balances_neg = dict_split(balances)
            debtor = choice(list(balances_pos.items()))
            creditor = choice(list(balances_neg.items()))
            amount = all_money(debtor, creditor)
            self.assertEqual(amount, debtor[1])
