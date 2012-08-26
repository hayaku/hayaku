# -*- coding: utf-8 -*-
#*_*#

import unittest

from probe import extract
from test_data import TESTS


class AbbrTests(unittest.TestCase):
    def is_eq(self, hayaku, test_value):
        if hayaku[1] is None:
            hayaku = hayaku[0], ''
        hayaku = '{0} {1}'.format(hayaku[0], hayaku[1]).strip()
        self.assertEqual(hayaku, test_value, "hayaku: '{0}' and test: '{1}'".format(hayaku, test_value))

if __name__ == '__main__':
    # filtered = ((abbr, value) for abbr, value in cases if ': ;' in value) # функция без значений
    filtered = ((abbr, value) for abbr, value in TESTS)

    # http://stackoverflow.com/questions/1193909/pythons-unittest-and-dynamic-creation-of-test-cases
    def ch(a, b):
        return lambda self: self.is_eq(a, b)

    for k, v in filtered:
        # print k, v 
        if '-' in k:
            continue
        # v = v[:v.find(':')]
        v = v.replace(';', '')
        v = v.replace(':', '')
        v = v.strip()
        if not v[0].isalpha():
            continue
        name = 'test_{0}'.format(k)
        setattr(AbbrTests, name, ch(extract(k), v))

    unittest.main()
