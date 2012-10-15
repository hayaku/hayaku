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

    def test_2(self):
        args = {'property-name': 'width', 'default-value': '100%', 'important': False, 'abbr': 'w0', 'type-value': 0}
        self.assertEqual(expand_value(args), '0')

    def test_3(self):
        args = {'property-name': 'width', 'default-value': '100%', 'important': False, 'abbr': 'w0p', 'type-value': 0, 'type-name': 'p'}
        self.assertEqual(expand_value(args), '0')

    def test_4(self):
        args = {'property-name': 'width', 'default-value': '100%', 'important': False, 'abbr': 'w0px', 'type-value': 0, 'type-name': 'px'}
        self.assertEqual(expand_value(args), '0')


if __name__ == '__main__':
    unittest.main()
