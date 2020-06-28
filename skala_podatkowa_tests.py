"""
Author: Dominik Dąbek
"""

import unittest
import skala_podatkowa
from decimal import *


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tax_payer = skala_podatkowa.TaxPeriod()

    def _test_tax_basis(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_basis(),
                         msg="Błąd wyliczenia podstawy podatku")

    def _test_tax(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax(),
                         msg="Błąd wyliczenia podatku")

    def _test_tax_free_amount_end_of_year(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_free_amount_end_of_year(),
                         msg="Błąd wyliczenia kwoty zmniejszającej podatek na koniec roku")

    def _test_tax_free_amount(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_free_amount(),
                         msg="Błąd wyliczenia kwoty zmniejszającej podatek")

    def _test_tax_owed(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_owed(),
                         msg="Błąd wyliczenia zaliczki do zapłaty")

    def _test_tax_owed_end_of_year(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_owed_end_of_year(),
                         msg="Błąd wyliczenia podatku na koniec roku")

    def _test_tax_owed_rounded(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_owed_rounded(),
                         msg="Błąd wyliczenia zaokrąglonej zaliczki do zapłaty")

    def _test_tax_owed_end_of_year_rounded(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_owed_end_of_year_rounded(),
                         msg="Błąd wyliczenia zaokrąglonego podatku na koniec roku")


class InitialData(BaseTestCase):
    def test_initial_values(self):
        self.assertEqual(0, self.tax_payer.expenses)
        self.assertEqual(0, self.tax_payer.revenue)
        self.assertEqual(0, self.tax_payer.tax_reduction)
        self.assertEqual(0, self.tax_payer.income_reduction)

    def test_initial_calculations(self):
        self._test_tax_basis('0')
        self._test_tax('0')
        self._test_tax_free_amount('525.12')
        self._test_tax_free_amount_end_of_year('1360')
        self._test_tax_owed('0')
        self._test_tax_owed_end_of_year('0')
        self._test_tax_owed_rounded('0')


class TestCase1(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tax_payer.revenue = Decimal('26433')
        self.tax_payer.expenses = Decimal('16416.65')
        self.tax_payer.tax_reduction = Decimal('624.04')

    def test_tax_basis(self):
        self._test_tax_basis('10016.35')

    def test_tax(self):
        self._test_tax('1702.72')

    def test_tax_free_amount(self):
        self._test_tax_free_amount('525.12')

    def test_tax_free_amount_end_of_year(self):
        self._test_tax_free_amount_end_of_year('1023.38')

    def test_tax_owed(self):
        self._test_tax_owed('553.56')

    def test_tax_owed_end_of_year(self):
        self._test_tax_owed_end_of_year('55.3')

    def test_tax_owed_rounded(self):
        self._test_tax_owed_rounded('554')

    def test_tax_owed_end_of_year_rounded(self):
        self._test_tax_owed_end_of_year_rounded('55')


class TestCase2(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tax_payer.revenue = Decimal('11300')
        self.tax_payer.expenses = Decimal('1153.73')
        self.tax_payer.tax_reduction = Decimal('918.82')
        self.tax_payer.income_reduction = Decimal('652.41')

    def test_tax_basis(self):
        self._test_tax_basis('9493.86')

    def test_tax(self):
        self._test_tax('1613.98')

    def test_tax_free_amount(self):
        self._test_tax_free_amount('525.12')

    def test_tax_free_amount_end_of_year(self):
        self._test_tax_free_amount_end_of_year('1110.54')

    def test_tax_owed(self):
        self._test_tax_owed('170.04')

    def test_tax_owed_end_of_year(self):
        self._test_tax_owed_end_of_year('0')

    def test_tax_owed_rounded(self):
        self._test_tax_owed_rounded('170')

    def test_tax_owed_end_of_year_rounded(self):
        self._test_tax_owed_end_of_year_rounded('0')


class Test100k(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tax_payer.revenue = Decimal('100000')

    def test_tax_basis(self):
        self._test_tax_basis('100000')

    def test_tax(self):
        self._test_tax('19170.80')

    def test_tax_free_amount(self):
        self._test_tax_free_amount('0')

    def test_tax_free_amount_end_of_year(self):
        self._test_tax_free_amount_end_of_year('341.88')

    def test_tax_owed(self):
        self._test_tax_owed('19170.80')

    def test_tax_owed_end_of_year(self):
        self._test_tax_owed_end_of_year('18828.92')

    def test_tax_owed_rounded(self):
        self._test_tax_owed_rounded('19171')

    def test_tax_owed_rounded_end_of_year(self):
        self._test_tax_owed_end_of_year_rounded('18829')


class Test150k(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tax_payer.revenue = Decimal('150000')
        self.tax_payer.expenses = Decimal('10000')
        self.tax_payer.tax_reduction = Decimal('1200')
        self.tax_payer.income_reduction = Decimal('900')
        self.tax_payer.tax_prepayment = Decimal('60')

    def test_tax_basis(self):
        self._test_tax_basis('139100')

    def test_tax(self):
        self._test_tax('31682.80')

    def test_tax_free_amount(self):
        self._test_tax_free_amount('0')

    def test_tax_free_amount_end_of_year(self):
        self._test_tax_free_amount_end_of_year('0')

    def test_tax_owed(self):
        self._test_tax_owed('30422.80')

    def test_tax_owed_end_of_year(self):
        self._test_tax_owed_end_of_year('30422.80')

    def test_tax_owed_rounded(self):
        self._test_tax_owed_rounded('30423')

    def test_tax_owed_rounded_end_of_year(self):
        self._test_tax_owed_end_of_year_rounded('30423')


if __name__ == '__main__':
    unittest.main()
