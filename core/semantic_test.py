# -*- coding: utf-8 -*-
import unittest

from probe import hayaku_extract

class SematicAbbrTests(unittest.TestCase):
    def test_0(self):
        self.assertEqual(hayaku_extract('fs'), 'font-size')

    def test_1(self):
        self.assertEqual(hayaku_extract('fst'), 'font-style')

    def test_2(self):
        self.assertEqual(hayaku_extract('w1'), 'width: 1px')

    def test_3(self):
        self.assertEqual(hayaku_extract('w1p'), 'width: 1px')

    def test_4(self):
        self.assertEqual(hayaku_extract('w1px'), 'width: 1px')

    def test_5(self):
        self.assertEqual(hayaku_extract('w1.1'), 'width: 1.1em')

    def test_6(self):
        self.assertEqual(hayaku_extract('w.1'), 'width: .1em')

    def test_7(self):
        self.assertEqual(hayaku_extract('w1.0'), 'width: 1em')

    def test_8(self):
        self.assertEqual(hayaku_extract('w1.'), 'width: 1em')

    def test_9(self):
        self.assertEqual(hayaku_extract('w1e'), 'width: 1em')

    def test_10(self):
        self.assertEqual(hayaku_extract('m-1'), 'margin: -1px')

    def test_11(self):
        self.assertEqual(hayaku_extract('m-.1'), 'margin: -.1em')

    def test_12(self):
        self.assertEqual(hayaku_extract('m0'), 'margin: 0')

    def test_13(self):
        self.assertEqual(hayaku_extract('m0.0'), 'margin: 0')

    def test_14(self):
        self.assertEqual(hayaku_extract('m-0.0'), 'margin: 0')

    def test_15(self):
        self.assertEqual(hayaku_extract('h1.100'), 'height: 1.1em')

    def test_16(self):
        self.assertEqual(hayaku_extract('p1m'), 'padding: 1mm')

    def test_17(self):
        self.assertEqual(hayaku_extract('p1%'), 'padding: 1%')

    def test_18(self):
        self.assertEqual(hayaku_extract('p.23pe'), 'padding: .23%')

    def test_19(self):
        self.assertEqual(hayaku_extract('p2.p'), 'padding: 2px')

    def test_20(self):
        self.assertEqual(hayaku_extract('p2.3p'), 'padding: 2.3px')

    def test_21(self):
        self.assertEqual(hayaku_extract('p3x'), 'padding: 3ex')

    def test_22(self):
        self.assertEqual(hayaku_extract('p3w'), 'padding: 3vw')

    def test_23(self):
        self.assertEqual(hayaku_extract('p3h'), 'padding: 3vh')

    def test_24(self):
        self.assertEqual(hayaku_extract('p3c'), 'padding: 3ch')

    def test_25(self):
        self.assertEqual(hayaku_extract('p3r'), 'padding: 3rem')

    def test_26(self):
        self.assertEqual(hayaku_extract('p3i'), 'padding: 3in')

    def test_27(self):
        self.assertEqual(hayaku_extract('p3t'), 'padding: 3pt')

    def test_28(self):
        self.assertEqual(hayaku_extract('b2'), 'bottom: 2px')

    def test_29(self):
        self.assertEqual(hayaku_extract('bd2'), 'border: 2px')

    def test_30(self):
        self.assertEqual(hayaku_extract('bw'), 'border-width: 2px')

    def test_31(self):
        self.assertEqual(hayaku_extract('blw'), 'border-left-width: 2px')

    def test_32(self):
        self.assertEqual(hayaku_extract('bdF'), 'border: #FFF')

    def test_33(self):
        self.assertEqual(hayaku_extract('bdF'), 'border: #FFF')

    def test_34(self):
        self.assertEqual(hayaku_extract('bd#0'), 'border: #000')

    def test_35(self):
        self.assertEqual(hayaku_extract('baF'), 'background: #FFF')

    def test_36(self):
        self.assertEqual(hayaku_extract('ba#f'), 'background: #FFF')

    def test_37(self):
        self.assertEqual(hayaku_extract('ba3'), 'background: #333')

    def test_38(self):
        self.assertEqual(hayaku_extract('ba3p'), 'background: 3px')

    def test_39(self):
        self.assertEqual(hayaku_extract('c00'), 'color: #000')

    def test_40(self):
        self.assertEqual(hayaku_extract('c02'), 'color: #000')

    def test_41(self):
        self.assertEqual(hayaku_extract('z1'), 'zoom: 1')

    def test_42(self):
        self.assertEqual(hayaku_extract('zi1'), 'z-index: 1')

    def test_43(self):
        self.assertEqual(hayaku_extract('zi-4'), 'z-index: -4')

    def test_44(self):
        self.assertEqual(hayaku_extract('fs4'), 'font-size: 4px')

    def test_issue_83_1(self):
        self.assertEqual(hayaku_extract('co'), 'color')

    def test_issue_83_2(self):
        self.assertEqual(hayaku_extract('con'), 'content')

    def test_issue_83_3(self):
        self.assertEqual(hayaku_extract('conn'), 'content: normal;')

    def test_issue_76_1(self):
        self.assertEqual(hayaku_extract('text-decoration'), 'text-decoration')

    def test_issue_76_2(self):
        self.assertEqual(hayaku_extract('border'), 'border')

if __name__ == '__main__':
    unittest.main()
