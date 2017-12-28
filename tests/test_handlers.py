import unittest
from unittest.mock import Mock

from handlers import add, show
from tutils import *


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # Create test chat with id equals to -1
        self.chat = set_or_create_chat()
        self.message = Mock()
        self.message.chat = self.chat

    def test_show(self):
        self.assertEqual(show(self.message, '1'), 'No results')

    def test_add(self):
        add(self.message, test_users[0], test_users[1], "10", "EUR")
        add(self.message, test_users[0], test_users[1], "5", "EUR")
        add(self.message, test_users[0], test_users[2], "15", "EUR")

        self.assertNotEqual(show(self.message, '1'), 'No results')

        self.assertEqual(len(show(self.message, '1').split('\n')), 1)
        self.assertEqual(show(self.message, '0'), "No results")
        # self.assertEqual(show(self.message, '-1'), "No results")

        self.assertEqual(len(show(self.message, test_users[0]).split('\n')), 3)
        self.assertEqual(len(show(self.message, test_users[1]).split('\n')), 2)
        self.assertEqual(len(show(self.message, test_users[2]).split('\n')), 1)
        self.assertNotEqual(show(self.message, test_users[2]), 'No results')

        self.assertEqual(len(show(self.message, test_users[0], '1').split('\n')), 1)
        self.assertEqual(len(show(self.message, test_users[0], '2').split('\n')), 2)
        self.assertEqual(len(show(self.message, test_users[0], '3').split('\n')), 3)
        self.assertEqual(len(show(self.message, '20', test_users[1]).split('\n')), 2)
        self.assertEqual(len(show(self.message, test_users[2], '10').split('\n')), 1)
        self.assertNotEqual(show(self.message, test_users[2], '10'), 'No results')

        self.assertEqual(len(show(self.message, test_users[0], test_users[1]).split('\n')), 2)
        self.assertEqual(show(self.message, test_users[2], test_users[1]), 'No results')

    def tearDown(self):
        destroy_chat()
