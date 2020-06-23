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

    def _test_tax_free_amount(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_free_amount(),
                         msg="Błąd wyliczenia kwoty zmniejszającej podatek")

    def _test_tax_owed(self, expected):
        self.assertEqual(Decimal(expected), self.tax_payer.tax_owed(),
                         msg="Błąd wyliczenia zaliczki do zapłaty")


class InitialData(BaseTestCase):
    def test_initial_values(self):
        self.assertEqual(0, self.tax_payer.expenses)
        self.assertEqual(0, self.tax_payer.revenue)
        self.assertEqual(0, self.tax_payer.tax_reduction)
        self.assertEqual(0, self.tax_payer.income_reduction)

    def test_initial_calculations(self):
        self._test_tax_basis('0')
        self._test_tax('0')
        self._test_tax_free_amount('1360')
        self._test_tax_owed('0')


class TestWfirma11205578(BaseTestCase):
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
        self._test_tax_free_amount('1023.38')

    def test_tax_owed(self):
        self._test_tax_owed('55.3')


class TestWfirma11181897(BaseTestCase):
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
        self._test_tax_free_amount('1110.54')

    def test_tax_owed(self):
        self._test_tax_owed('0')


class AboveThreshold(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tax_payer.revenue = Decimal('100000')

    def test_tax_basis(self):
        self._test_tax_basis('100000')

    def test_tax(self):
        self._test_tax('19170.80')

    def test_tax_free_amount(self):
        self._test_tax_free_amount('341.88')

    def test_tax_owed(self):
        self._test_tax_owed('18828.92')


if __name__ == '__main__':
    unittest.main()
