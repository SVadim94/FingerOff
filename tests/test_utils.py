import unittest

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
        self.chat = set_or_create_chat()

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

    def test_subset_sum(self):
        for _ in range(100):
            balances, ss = generate_test_set()
            group = subset_sum(balances, ss)
            self.assertEqual(sum(balances[user] for user in group), ss)
