# -*- coding: utf-8 -*-
import unittest

from templates import expand_value
from probe import extract

class ExpandValueTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(expand_value(extract('z8')), '8')

    def test_1(self):
        self.assertEqual(expand_value(extract('zi12')), '12')

    def test_2(self):
        self.assertEqual(expand_value(extract('w0')), '0')

    def test_3(self):
        self.assertEqual(expand_value(extract('w0p')), '0')

    def test_4(self):
        self.assertEqual(expand_value(extract('w0px')), '0')


if __name__ == '__main__':
    unittest.main()
