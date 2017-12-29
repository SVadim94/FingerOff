import unittest
from unittest.mock import Mock

from handlers import *
from tutils import *


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # Create test chat with id equals to -1
        self.chat = set_or_create_chat()
        self.message = Mock()
        self.message.chat = self.chat
        self.add = lambda f, t, a: add(self.message, test_users[f], test_users[t], str(a))
        self.assertLinesCount = lambda args, lines: self.assertEqual(
            len(show(self.message, *args).split('\n')),
            lines
        )

    def test_add(self):
        count = lambda: Transaction.select().where(Transaction.chat == self.chat).count()

        self.add(0, 1, 10)
        self.assertEqual(count(), 1)

        self.add(0, 1, 5)
        self.assertEqual(count(), 2)

        self.add(0, 2, 15)
        self.assertEqual(count(), 3)

    def test_show(self):
        self.add(0, 1, 10)
        self.add(0, 1, 5)
        self.add(0, 2, 15)

        self.assertNotEqual(show(self.message, '1'), 'No results')

        self.assertLinesCount(['1'], 1)
        self.assertEqual(show(self.message, '0'), "No results")
        # self.assertEqual(show(self.message, '-1'), "No results")

        self.assertLinesCount([test_users[0]], 3)
        self.assertLinesCount([test_users[1]], 2)
        self.assertLinesCount([test_users[2]], 1)
        self.assertNotEqual(show(self.message, test_users[2]), 'No results')

        self.assertLinesCount([test_users[0], '1'], 1)
        self.assertLinesCount([test_users[0], '2'], 2)
        self.assertLinesCount([test_users[0], '3'], 3)
        self.assertLinesCount(['20', test_users[1]], 2)
        self.assertLinesCount([test_users[2], '10'], 1)
        self.assertNotEqual(show(self.message, test_users[2], '10'), 'No results')

        self.assertLinesCount([test_users[0], test_users[1]], 2)
        self.assertEqual(show(self.message, test_users[2], test_users[1]), 'No results')

    def test_foff(self):
        for _ in range(100):
            balances = generate_test_set(True)

            UserBalance.delete().where(UserBalance.chat == self.chat)

            for k, v in balances.items():
                UserBalance.create(chat=self.chat, user=get_or_create_user(k), balance=v)

            self.assertNotEqual(list(UserBalance.select()), [])

            output = foff(self.message).split('\n')
            output = filter(lambda line: '/add' in line, output)

            for line in output:
                args = line.split(' ')[1:]
                add(self.message, *args)

            self.assertListEqual(list(UserBalance.select()), [])

    def test_annotated(self):
        self.assertFalse(check_annotated("handlers"))

    def tearDown(self):
        destroy_chat()
