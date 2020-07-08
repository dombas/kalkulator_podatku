"""
Author: Dominik Dąbek
"""

import unittest
from typing import List, Tuple

import skala_podatkowa
from decimal import *
from kalkulator_GUI import convert_input, strip_non_numeric, only_numeric, clean_input, save_inputs, load_inputs


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


class InputHandlingTestCase(unittest.TestCase):
    def _test_convert_input(self, inputs_expected: 'List[Tuple[str,str]]'):
        for input_value, expected in inputs_expected:
            self.assertEqual(
                Decimal(expected),
                convert_input(input_value))

    def test_strip_non_numeric(self):
        inputs_expected = [
            ('100', '100'),
            ('aa345bb', '345'),
            ('.123.34zł', '123.34'),
            ('5 600', '5 600')
        ]
        for input_value, expected in inputs_expected:
            self.assertEqual(
                expected,
                strip_non_numeric(input_value))

    def test_only_numeric(self):
        inputs_expected = [
            ('345', '345'),
            ('.123.34zł', '12334'),
            ('5 600', '5600')
        ]
        for input_value, expected in inputs_expected:
            self.assertEqual(
                expected,
                only_numeric(input_value))

    def test_clean_input(self):
        inputs_expected = [
            ('1 000,50', '1000.50'),
            ('6,954,555.20', '6954555.20'),
            ('12.343.222,50', '12343222.50'),
            ('1,23zł', '1.23'),
            ('600.30gbp', '600.30'),
        ]
        for input_value, expected in inputs_expected:
            self.assertEqual(
                expected,
                clean_input(input_value))

    def test_convert_input_short(self):
        inputs_expected = [
            ('0,', '0'),
            ('0.', '0')
        ]
        self._test_convert_input(inputs_expected)

    def test_separators(self):
        inputs_expected = [
            ('1,23', '1.23'),
            ('600.30', '600.30')
        ]
        self._test_convert_input(inputs_expected)

    def test_multiple_separators(self):
        inputs_expected = [
            ('1 000,50', '1000.50'),
            ('6,954,555.20', '6954555.20'),
            ('12.343.222,50', '12343222.50')
        ]
        self._test_convert_input(inputs_expected)

    def test_non_digit_characters(self):
        inputs_expected = [
            ('1,23zł', '1.23'),
            ('600.30gbp', '600.30')
        ]
        self._test_convert_input(inputs_expected)


class SavingLoadingTestCase(unittest.TestCase):
    def test_save_load(self):
        inputs_dict = {
            'revenue': '2000',
            'expenses': '1000',
            'tax_reduction': '200',
            'income_reduction': '100',
            'tax_prepayment': '50'
        }
        save_inputs(inputs_dict)
        loaded_dict = load_inputs()
        self.assertDictEqual(inputs_dict, loaded_dict, "Błąd zapisu danych")


if __name__ == '__main__':
    unittest.main()
