# -*- coding: utf-8 -*-
import unittest

from css_dict_driver import expand_values, parse_dict, FILE_DATA

class CssDictTests(unittest.TestCase):

    def test_0(self):
        pd = parse_dict(FILE_DATA)
        self.assertEqual(expand_values(pd, pd.keys())['caption-side'], set(['top', 'bottom']))

    def test_1(self):
        pd = parse_dict(FILE_DATA)
        self.assertEqual(expand_values(pd, pd.keys())['width'], set([
            'auto', '<dimension>', "['100%']",
            '<number>', '<length>', '<percentage>',
            '.em', '.ex', '.vw', '.vh', '.vm', '.ch', '.rem',
            '.px', '.cm', '.mm', '.in', '.pt', '.pc', '.%',
            ]))


if __name__ == '__main__':
    unittest.main()
