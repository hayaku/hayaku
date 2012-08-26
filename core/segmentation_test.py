# -*- coding: utf-8 -*-
import unittest

from probe import segmentation
from templates import color_expand


class AbbrTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(segmentation('poa'), ('poa', None, False, False))

    def test_1(self):
        self.assertEqual(segmentation('c#FA5EC1'), ('c', '#FA5EC1', True, False))

    def test_2(self):
        self.assertEqual(segmentation('c0'), ('c', '0', True, False))

    def test_3(self):
        self.assertEqual(segmentation('c#fe'), ('c', '#fe', True, False))

    def test_4(self):
        self.assertEqual(segmentation('cFE'), ('c', 'FE', True, False))

    def test_5(self):
        self.assertEqual(segmentation('ml10'), ('ml', '10', True, False))

    def test_6(self):
        self.assertEqual(segmentation('p-.5'), ('p', '-.5', True, False))

    def test_7(self):
        self.assertEqual(segmentation('h2p'), ('h', '2p', True, False))

    def test_8(self):
        self.assertEqual(segmentation('h2pe'), ('h', '2pe', True, False))

    def test_9(self):
        self.assertEqual(segmentation('h2pt'), ('h', '2pt', True, False))

    def test_10(self):
        self.assertEqual(segmentation('h!'), ('h', None, False, True))

    def test_11(self):
        self.assertEqual(segmentation('poa'), ('poa', None, False, False))

    def test_12(self):
        self.assertEqual(segmentation('posa'), ('posa', None, False, False))

    def test_13(self):
        self.assertEqual(segmentation('po:a'), ('po', 'a', False, False))

    def test_14(self):
        self.assertEqual(segmentation('pos:a'), ('pos', 'a', False, False))

    def test_15(self):
        self.assertEqual(segmentation('pos:'), ('pos', '', False, False))

    def test_16(self):
        self.assertEqual(segmentation('poa!'), ('poa', None, False, True))

    def test_17(self):
        self.assertEqual(segmentation('posa!'), ('posa', None, False, True))

    def test_18(self):
        self.assertEqual(segmentation('po:a!'), ('po', 'a', False, True))

    def test_19(self):
        self.assertEqual(segmentation('pos:a!'), ('pos', 'a', False, True))

    def test_20(self):
        self.assertEqual(segmentation('pos:!'), ('pos', '', False, True))

    def test_21(self):
        self.assertEqual(segmentation('h'), ('h', None, False, False))

    def test_22(self):
        self.assertEqual(segmentation('h:'), ('h', '', False, False))

    def test_23(self):
        self.assertEqual(segmentation('c:#FA5EC1'), ('c', '#FA5EC1', True, False))

    def test_24(self):
        self.assertEqual(segmentation('c:0'), ('c', '0', True, False))

    def test_25(self):
        self.assertEqual(segmentation('c:#fe'), ('c', '#fe', True, False))

    def test_26(self):
        self.assertEqual(segmentation('c:FE'), ('c', 'FE', True, False))

    def test_27(self):
        self.assertEqual(segmentation('ml:10'), ('ml', '10', True, False))

    def test_28(self):
        self.assertEqual(segmentation('p:-.5'), ('p', '-.5', True, False))

    def test_29(self):
        self.assertEqual(segmentation('h:2p'), ('h', '2p', True, False))

    def test_30(self):
        self.assertEqual(segmentation('h:2pe'), ('h', '2pe', True, False))

    def test_31(self):
        self.assertEqual(segmentation('h:2pt'), ('h', '2pt', True, False))

    def test_32(self):
        self.assertEqual(segmentation('h-t2pt'), ('h-t', '2pt', True, False))

    def test_33(self):
        self.assertEqual(segmentation('c0'), ('c', '0', True, False))

    def test_34(self):
        self.assertEqual(segmentation('w10.'), ('w', '10.', True, False))

    def test_35(self):
        self.assertEqual(segmentation('c#'), ('c', '#', True, False))

    def test_36(self):
        self.assertEqual(segmentation('w:10.'), ('w', '10.', True, False))

    def test_37(self):
        self.assertEqual(segmentation('c:#'), ('c', '#', True, False))

    def test_38(self):
        self.assertEqual(segmentation('w.0'), ('w', '.0', True, False))

    def test_39(self):
        self.assertEqual(segmentation('c:f'), ('c', 'f', False, False))


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


if __name__ == '__main__':
    unittest.main()
