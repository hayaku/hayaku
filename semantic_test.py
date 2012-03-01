# -*- coding: utf-8 -*-
import unittest

from probe import hayaku_extract

class SematicAbbrTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(hayaku_extract('fst4'), 'font-size: 4px')

    def test_1(self):
        self.assertEqual(hayaku_extract('fst'), 'font-style')


if __name__ == '__main__':
    unittest.main()
