# -*- coding: utf-8 -*-
import unittest

from templates import expand_value

class ValuesTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(expand_value('zoom', '1'), '1')

    def test_1(self):
        self.assertEqual(expand_value('width', '10'), '10px')

    def test_2(self):
        self.assertEqual(expand_value('font-size', '10'), '10px')


if __name__ == '__main__':
    unittest.main()
