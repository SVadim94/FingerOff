import unittest

from utils import is_int, join_columns


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
