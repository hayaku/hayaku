# -*- coding: utf-8 -*-
import unittest

from templates import expand_value
from probe import extract

class ExpandValueTests(unittest.TestCase):
    def setUp(self):
        self.opts = {
           'hayaku_CSS_default_unit': 'px',
           'hayaku_CSS_default_unit_decimal': 'em',
        }

    def test_0(self):
        self.assertEqual(expand_value(extract('z8')), '8')

    def test_1(self):
        self.assertEqual(expand_value(extract('zi12')), '12')


    # TODO: что делать для w0.0 w.0 w0.p w.0p ...
    def test_2(self):
        self.assertEqual(expand_value(extract('w0'), self.opts), '0')

    def test_3(self):
        self.assertEqual(expand_value(extract('w0p'), self.opts), '0')

    def test_4(self):
        self.assertEqual(expand_value(extract('w0px'), self.opts), '0')


    def test_5(self):
        self.assertEqual(expand_value(extract('w'), self.opts), '[100%]')

    def test_6(self):
        self.assertEqual(expand_value(extract('w10%')), '10%')

    def test_7(self):
        self.assertEqual(expand_value(extract('w10perc'), self.opts), '10%')

    def test_8(self):
        self.assertEqual(expand_value(extract('vat')), 'top')

    # Тесты 9 и 10 не должены генерировать ошибки
    def test_9(self):
        self.assertEqual(expand_value(extract('w')), '[100%]')

    def test_10(self):
        self.assertEqual(expand_value(extract('w'), {}), '[100%]')

    def test_11(self):
        self.assertEqual(expand_value(extract('c#')), '#')

if __name__ == '__main__':
    unittest.main()
