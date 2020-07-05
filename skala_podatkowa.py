"""
Author: Dominik Dąbek
"""

from decimal import *


def list_to_decimal(list_of_str: 'List[str]') -> 'List[Decimal]':
    list_of_decimals = []
    for s in list_of_str:
        list_of_decimals.append(Decimal(s))
    return list_of_decimals


def round_cents(dec: 'Decimal') -> 'Decimal':
    return dec.quantize(Decimal('.01'))


def round_whole(dec: 'Decimal') -> 'Decimal':
    return dec.quantize(Decimal('1'))


class TaxPeriod:
    """Calculates tax owed
    https://ksiegowosc.infor.pl/podatki/pit/pit/rozliczenia/3063125,2,PIT-2020-skala-podatkowa-stawki-i-koszty-uzyskania-przychodu.html"""
    BEFORE_THRESHOLD_TAX = Decimal('0.17')
    THRESHOLD = Decimal('85528')
    AFTER_THRESHOLD_TAX = Decimal('0.32')
    AFTER_THRESHOLD_CONSTANT = Decimal('14539.76')
    TAX_FREE_AMOUNT_THRESHOLDS = list_to_decimal(['8000', '13000', '85528', '127000'])
    TAX_FREE_AMOUNT_CONSTANTS = list_to_decimal(['1360', '834.88', '5000', '525.12', '41472'])

    def __init__(self):
        self.revenue = Decimal('0')  # przychód
        self.expenses = Decimal('0')  # koszty
        self.tax_reduction = Decimal('0')  # odliczenia od podatku
        self.income_reduction = Decimal('0')  # odliczenia od dochodu
        self.tax_prepayment = Decimal('0')  # zapłacone zaliczki

    def set_revenue(self, value_to_set: 'Decimal'):
        self.revenue = value_to_set

    def set_expenses(self, value_to_set: 'Decimal'):
        self.expenses = value_to_set

    def set_tax_reduction(self, value_to_set: 'Decimal'):
        self.tax_reduction = value_to_set

    def set_income_reduction(self, value_to_set: 'Decimal'):
        self.income_reduction = value_to_set

    def set_tax_prepayment(self, value_to_set: 'Decimal'):
        self.tax_prepayment = value_to_set

    def income(self) -> 'Decimal':
        return self.revenue - self.expenses

    def tax_basis(self) -> 'Decimal':
        return Decimal(self.income() - self.income_reduction)

    def tax_free_amount(self) -> 'Decimal':
        tax_basis = round_whole(self.tax_basis())
        tax_free_amount = Decimal('0')
        if self.TAX_FREE_AMOUNT_THRESHOLDS[2] >= tax_basis:
            tax_free_amount = self.TAX_FREE_AMOUNT_CONSTANTS[3]
        return tax_free_amount

    def tax_free_amount_end_of_year(self) -> Decimal:
        tax_basis = round_whole(self.tax_basis())
        tax_free_amount = Decimal('0')
        if self.TAX_FREE_AMOUNT_THRESHOLDS[0] >= tax_basis:
            tax_free_amount = self.TAX_FREE_AMOUNT_CONSTANTS[0]
        elif self.TAX_FREE_AMOUNT_THRESHOLDS[1] >= tax_basis:
            tax_free_amount = self.TAX_FREE_AMOUNT_CONSTANTS[0] - \
                              (self.TAX_FREE_AMOUNT_CONSTANTS[1] *
                               (tax_basis - self.TAX_FREE_AMOUNT_THRESHOLDS[0]) /
                               self.TAX_FREE_AMOUNT_CONSTANTS[2])
        elif self.TAX_FREE_AMOUNT_THRESHOLDS[2] >= tax_basis:
            tax_free_amount = self.TAX_FREE_AMOUNT_CONSTANTS[3]
        elif self.TAX_FREE_AMOUNT_THRESHOLDS[3] >= tax_basis:
            tax_free_amount = self.TAX_FREE_AMOUNT_CONSTANTS[3] - \
                              (self.TAX_FREE_AMOUNT_CONSTANTS[3] *
                               (tax_basis - self.TAX_FREE_AMOUNT_THRESHOLDS[2]) /
                               self.TAX_FREE_AMOUNT_CONSTANTS[4])
        return round_cents(tax_free_amount)

    def tax(self) -> 'Decimal':
        tax = Decimal('0')
        tax_basis = round_whole(self.tax_basis())
        if self.THRESHOLD >= tax_basis:
            tax = tax_basis * self.BEFORE_THRESHOLD_TAX
        else:
            over_threshold = tax_basis - self.THRESHOLD
            tax += self.AFTER_THRESHOLD_CONSTANT
            tax += over_threshold * self.AFTER_THRESHOLD_TAX
        return round_cents(tax)

    def tax_owed(self) -> 'Decimal':
        tax_owed = self.tax()
        tax_owed -= self.tax_reduction
        tax_owed -= self.tax_free_amount()
        tax_owed -= self.tax_prepayment
        if 0 > tax_owed:
            tax_owed = Decimal('0')
        return tax_owed

    def tax_owed_end_of_year(self) -> 'Decimal':
        tax_owed = self.tax()
        tax_owed -= self.tax_reduction
        tax_owed -= self.tax_free_amount_end_of_year()
        tax_owed -= self.tax_prepayment
        if 0 > tax_owed:
            tax_owed = Decimal('0')
        return tax_owed

    def tax_owed_rounded(self) -> 'Decimal':
        return round_whole(self.tax_owed())

    def tax_owed_end_of_year_rounded(self) -> 'Decimal':
        return round_whole(self.tax_owed_end_of_year())
        pass
