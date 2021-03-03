from unittest import TestCase
from . import example as e

class MyTest(TestCase):
    
    def test_add_number_if_odd(self):
        self.assertEqual(e.add_number_if_odd(1, 2), 1)
        self.assertEqual(e.add_number_if_odd(1, 0), 1)
        self.assertEqual(e.add_number_if_odd(1, 3), 4)
    
    def test_add_number_if_odd_none_input(self):
        self.assertEqual(e.add_number_if_odd(None, 1), 1)
        self.assertEqual(e.add_number_if_odd(1, None), 1)