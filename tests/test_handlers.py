import unittest
from unittest.mock import Mock

from handlers import show, add

from tutils import destroy_chat, set_or_create_chat


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # Create test chat with id equals to -1
        self.chat = set_or_create_chat(id=-1, inited=True)
        self.message = Mock()
        self.message.chat = self.chat

    def test_show(self):
        self.assertEqual(show(self.message, '1'), 'No results')

    def test_add(self):
        add(self.message, "@Pupa", "@Lupa", "10", "EUR")
        add(self.message, "@Pupa", "@Lupa", "5", "EUR")
        add(self.message, "@Pupa", "@Buhg", "15", "EUR")
        
        self.assertNotEqual(show(self.message, '1'), 'No results')
        
        self.assertEqual(len(show(self.message, '1').split('\n')), 3)
        self.assertEqual(len(show(self.message, '0').split('\n')), 3)
        self.assertEqual(show(self.message, '-1'), "No results")
        
        self.assertEqual(len(show(self.message, '@Pupa').split('\n')), 3)
        self.assertEqual(len(show(self.message, '@Lupa').split('\n')), 2)
        self.assertEqual(len(show(self.message, '@Buhg').split('\n')), 1)

        self.assertEqual(len(show(self.message, '@Pupa', '1').split('\n')), 3)
        self.assertEqual(len(show(self.message, '2', '@Lupa').split('\n')), 2)
        self.assertEqual(len(show(self.message, '@Buhg', '10').split('\n')), 1)
        self.assertNotEqual(show(self.message, '@Buhg', '10'), 'No results')

    def tearDown(self):
        destroy_chat()
