# -*- coding: utf-8 -*-
import unittest

from templates import expand_value

class ExpandValueTests(unittest.TestCase):
    def test_0(self):
        args = {'property-name': 'zoom', 'important': False, 'abbr': 'z8', 'type-value': 8}
        self.assertEqual(expand_value(args), '8')

    def test_1(self):
        args = {'property-name': 'z-index', 'important': False, 'abbr': 'zi2', 'type-value': 2}
        self.assertEqual(expand_value(args), '2')


if __name__ == '__main__':
    unittest.main()
