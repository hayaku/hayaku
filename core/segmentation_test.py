# -*- coding: utf-8 -*-
import unittest

from probe import segmentation, extract
from templates import color_expand

class ExtractTests(unittest.TestCase):
    # похоже что дубль для semantic_test.py
    def test_0(self):
        pass
        # self.assertEqual(extract('poa'), {'color': 'f', 'value': 'F', 'property_extracted': 'color', 'important': False, 'abbr': 'cF', 'property': 'c', 'value_extracted': "['#FFF']"})
        # self.assertEqual(extract('poa'), {'color': 'e', 'value': 'E', 'property_extracted': '', 'important': False, 'abbr': 'cE', 'property': 'c'})
        # self.assertEqual(extract('cF')['property_extracted'], 'color')
        # self.assertEqual(extract('cE')['property_extracted'], 'color')

class AbbrTests(unittest.TestCase):

    def test_0(self):
        self.assertEqual(segmentation('poa'), {'property-value': 'poa', 'important': False, 'abbr': 'poa'})

    def test_1(self):
        self.assertEqual(segmentation('c#FA5EC1'),
            {'property-name': 'c', 'important': False, 'abbr': 'c#FA5EC1', 'color': 'FA5EC1'})

    def test_2(self):
        self.assertEqual(segmentation('c0'),
            {'property-name': 'c', 'important': False, 'abbr': 'c0', 'color': '0', 'type-value': 0})

    def test_3(self):
        self.assertEqual(segmentation('c#fe'),
            {'property-name': 'c', 'important': False, 'abbr': 'c#fe', 'color': 'FE'})

    def test_4(self):
        self.assertEqual(segmentation('cFE'),
            {'property-name': 'c', 'important': False, 'abbr': 'cFE', 'color': 'FE'})

    def test_5(self):
        self.assertEqual(segmentation('ml10'),
            {'property-name': 'ml', 'important': False, 'abbr': 'ml10', 'type-value': 10, 'color': '10'})

    def test_6(self):
        self.assertEqual(segmentation('p-.5'),
            {'property-name': 'p', 'important': False, 'abbr': 'p-.5', 'type-value': -0.5})

    def test_7(self):
        self.assertEqual(segmentation('h2p'),
            {'property-name': 'h', 'important': False, 'abbr': 'h2p', 'type-value': 2, 'type-name': 'p'})

    def test_8(self):
        self.assertEqual(segmentation('h2pe'),
            {'property-name': 'h', 'important': False, 'abbr': 'h2pe', 'type-value': 2, 'type-name': 'pe'})

    def test_9(self):
        self.assertEqual(segmentation('h2pt'),
            {'property-name': 'h', 'important': False, 'abbr': 'h2pt', 'type-value': 2, 'type-name': 'pt'})

    def test_10(self):
        self.assertEqual(segmentation('h!'),
            {'property-value': 'h', 'important': True, 'abbr': 'h!'})

    def test_11(self):
        self.assertEqual(segmentation('poa'),
            {'property-value': 'poa', 'important': False, 'abbr': 'poa'})

    def test_12(self):
        self.assertEqual(segmentation('posa'),
            {'property-value': 'posa', 'important': False, 'abbr': 'posa'})

    def test_13(self):
        self.assertEqual(segmentation('po:a'),
            {'property-name': 'po', 'important': False, 'abbr': 'po:a', 'keyword-value': 'a'})

    def test_14(self):
        self.assertEqual(segmentation('pos:a'),
            {'property-name': 'pos', 'important': False, 'abbr': 'pos:a', 'keyword-value': 'a'})

    def test_15(self):
        self.assertEqual(segmentation('pos:'),
            {'property-name': 'pos', 'important': False, 'abbr': 'pos:'})

    def test_16(self):
        self.assertEqual(segmentation('poa!'),
            {'property-value': 'poa', 'important': True, 'abbr': 'poa!'})

    def test_17(self):
        self.assertEqual(segmentation('posa!'),
            {'property-value': 'posa', 'important': True, 'abbr': 'posa!'})

    def test_18(self):
        self.assertEqual(segmentation('po:a!'),
            {'property-name': 'po', 'important': True, 'abbr': 'po:a!', 'keyword-value': 'a'})

    def test_19(self):
        #todo: удалить тест, он такой же как 18
        self.assertEqual(segmentation('pos:a!'),
            {'property-name': 'pos', 'important': True, 'abbr': 'pos:a!', 'keyword-value': 'a'})

    def test_20(self):
        self.assertEqual(segmentation('pos:!'),
            {'property-name': 'pos', 'important': True, 'abbr': 'pos:!'})

    def test_21(self):
        self.assertEqual(segmentation('h'),
            {'property-value': 'h', 'important': False, 'abbr': 'h'})

    def test_22(self):
        self.assertEqual(segmentation('h:'),
            {'property-name': 'h', 'important': False, 'abbr': 'h:'})

    def test_23(self):
        self.assertEqual(segmentation('c:#FA5EC1'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:#FA5EC1', 'color': 'FA5EC1'})

    def test_24(self):
        self.assertEqual(segmentation('c:0'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:0', 'color': '0', 'type-value': 0})

    def test_25(self):
        self.assertEqual(segmentation('c:#fe'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:#fe', 'color': 'FE'})

    def test_26(self):
        self.assertEqual(segmentation('c:FE'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:FE', 'color': 'FE'})

    def test_27(self):
        self.assertEqual(segmentation('ml:10'),
            {'property-name': 'ml', 'important': False, 'abbr': 'ml:10', 'color': '10', 'type-value': 10})

    def test_28(self):
        self.assertEqual(segmentation('p:-.5'),
            {'property-name': 'p', 'important': False, 'abbr': 'p:-.5', 'type-value': -0.5})

    def test_29(self):
        self.assertEqual(segmentation('h:2p'),
            {'property-name': 'h', 'important': False, 'abbr': 'h:2p', 'type-value': 2,  'type-name': 'p'})

    def test_30(self):
        self.assertEqual(segmentation('h:2pe'),
            {'property-name': 'h', 'important': False, 'abbr': 'h:2pe', 'type-value': 2,  'type-name': 'pe'})

    def test_31(self):
        self.assertEqual(segmentation('h:2pt'),
            {'property-name': 'h', 'important': False, 'abbr': 'h:2pt', 'type-value': 2,  'type-name': 'pt'})

    def test_32(self):
        self.assertEqual(segmentation('h-t2pt'),
            {'property-name': 'h-t', 'important': False, 'abbr': 'h-t2pt', 'type-value': 2,  'type-name': 'pt'})

    def test_33(self):
        self.assertEqual(segmentation('c0'),
            {'property-name': 'c', 'important': False, 'abbr': 'c0', 'color': '0', 'type-value': 0})

    def test_34(self):
        self.assertEqual(segmentation('w10.'),
            {'property-name': 'w', 'important': False, 'abbr': 'w10.', 'type-value': 10.0})

    def test_35(self):
        self.assertEqual(segmentation('c#'),
            {'property-name': 'c', 'important': False, 'abbr': 'c#', 'color': ''})

    def test_36(self):
        self.assertEqual(segmentation('w:10.'),
            {'property-name': 'w', 'important': False, 'abbr': 'w:10.', 'type-value': 10.0})

    def test_37(self):
        self.assertEqual(segmentation('c:#'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:#', 'color': ''})

    def test_38(self):
        self.assertEqual(segmentation('w.0'),
            {'property-name': 'w', 'important': False, 'abbr': 'w.0', 'type-value': 0.0})

    def test_39(self):
        self.assertEqual(segmentation('c:f'),
            {'property-name': 'c', 'important': False, 'abbr': 'c:f', 'keyword-value': 'f'})

    # def test_40(self):
    # TODO: разобраться что делать с такими аббревиатурами, найти тикеты и т.д.
    #     "b-"
    #     self.assertEqual(segmentation('b-'), ('b', '-', False, False))

    def test_41(self):
        self.assertEqual(segmentation('c0F'),
            {'property-name': 'c', 'important': False, 'abbr': 'c0F', 'color': '0F'})

    def test_42(self):
        self.assertEqual(segmentation('c0F.5'),
            {'property-name': 'c', 'important': False, 'abbr': 'c0F', 'color': '0F', 'color_alpha': '.5'})

    def test_44(self):
        self.assertEqual(segmentation('w10%'),
            {'property-name': 'w', 'important': False, 'type-value': 10,
            'type-name': '%', 'abbr': 'w10%'})


class ColorSegmentationTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(color_expand('0'), '#000')

    def test_1(self):
        self.assertEqual(color_expand('#0'), '#000')

    def test_2(self):
        self.assertEqual(color_expand('C'), '#CCC')

    def test_3(self):
        self.assertEqual(color_expand('CF'), '#CFCFCF')

    def test_4(self):
        self.assertEqual(color_expand('#C'), '#CCC')

    def test_5(self):
        self.assertEqual(color_expand('#cf'), '#CFCFCF')

    def test_6(self):
        self.assertEqual(color_expand('#CF'), '#CFCFCF')

    def test_7(self):
        self.assertEqual(color_expand('#FFF'), '#FFF')

    def test_8(self):
        self.assertEqual(color_expand('#111'), '#111')

    def test_9(self):
        self.assertEqual(color_expand('111'), '#111')

    def test_10(self):
        self.assertEqual(color_expand('#f'), '#FFF')

    def test_11(self):
        self.assertEqual(color_expand('123456'), '#123456')

    def test_12(self):
        self.assertEqual(color_expand('abcdef'), '#ABCDEF')

    def test_13(self):
        self.assertEqual(color_expand('#0F'), '#0F0F0F')

    def test_14(self):
        self.assertEqual(color_expand('0F'), '#0F0F0F')

    def test_15(self):
        self.assertEqual(color_expand('0','.5'), 'rgba(0,0,0,.5)')

    def test_16(self):
        self.assertEqual(color_expand('F','.2'), 'rgba(255,255,255,.2)')

    def test_17(self):
        self.assertEqual(color_expand('ABCD'), 'rgba(170,187,204,0.87)')

    def test_18(self):
        self.assertEqual(color_expand('ABC80'), 'rgba(170,187,204,0.5)')


if __name__ == '__main__':
    unittest.main()
