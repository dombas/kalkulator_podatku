'''
Author: Dominik Dąbek
'''

from decimal import *

BEFORE_THRESHOLD_TAX = Decimal('0.17')
THRESHOLD = Decimal('85528')
AFTER_THRESHOLD_TAX = Decimal('0.32')
AFTER_THRESHOLD_CONSTANT = Decimal('14539.76')


def list_to_decimal(list_of_str):
    list_of_decimals = []
    for s in list_of_str:
        list_of_decimals.append(Decimal(s))
    return list_of_decimals


def round_cents(dec):
    return dec.quantize(Decimal('.01'))


def round_whole(dec):
    return dec.quantize(Decimal('1'))


class TaxPeriod:
    """Calculates tax owed
    https://ksiegowosc.infor.pl/podatki/pit/pit/rozliczenia/3063125,2,PIT-2020-skala-podatkowa-stawki-i-koszty-uzyskania-przychodu.html"""
    TAX_FREE_AMOUNT_THRESHOLDS = list_to_decimal(['8000', '13000', '85528', '127000'])
    TAX_FREE_AMOUNT_CONSTANTS = list_to_decimal(['1360', '834.88', '5000', '525.12', '41472'])

    revenue = Decimal('0')  # przychód
    expenses = Decimal('0')  # koszty
    tax_reduction = Decimal('0')  # odliczenia od podatku
    income_reduction = Decimal('0')  # odliczenia od dochodu
    tax_prepayment = Decimal('0')  # zapłacone zaliczki

    def income(self):
        return self.revenue - self.expenses

    def tax_basis(self):
        return Decimal(self.income() - self.income_reduction)

    def tax_free_amount(self):
        tax_basis = round_whole(self.tax_basis())
        tax_free_amount = Decimal('0')
        TAX_FREE_AMOUNT_THRESHOLDS = self.TAX_FREE_AMOUNT_THRESHOLDS
        TAX_FREE_AMOUNT_CONSTANTS = self.TAX_FREE_AMOUNT_CONSTANTS
        if TAX_FREE_AMOUNT_THRESHOLDS[0] >= tax_basis:
            tax_free_amount = TAX_FREE_AMOUNT_CONSTANTS[0]
        elif TAX_FREE_AMOUNT_THRESHOLDS[1] >= tax_basis:
            tax_free_amount = TAX_FREE_AMOUNT_CONSTANTS[0] - \
                              (TAX_FREE_AMOUNT_CONSTANTS[1] *
                               (tax_basis - TAX_FREE_AMOUNT_THRESHOLDS[0]) /
                               TAX_FREE_AMOUNT_CONSTANTS[2])
        elif TAX_FREE_AMOUNT_THRESHOLDS[2] >= tax_basis:
            tax_free_amount = TAX_FREE_AMOUNT_CONSTANTS[3]
        elif TAX_FREE_AMOUNT_THRESHOLDS[3] >= tax_basis:
            tax_free_amount = TAX_FREE_AMOUNT_CONSTANTS[3] - \
                              (TAX_FREE_AMOUNT_CONSTANTS[3] *
                               (tax_basis - TAX_FREE_AMOUNT_THRESHOLDS[2]) /
                               TAX_FREE_AMOUNT_CONSTANTS[4])
        return round_cents(tax_free_amount)

    def tax(self):
        tax = Decimal('0')
        tax_basis = round_whole(self.tax_basis())
        if THRESHOLD >= tax_basis:
            tax = tax_basis * BEFORE_THRESHOLD_TAX
        else:
            over_threshold = tax_basis - THRESHOLD
            tax += AFTER_THRESHOLD_CONSTANT
            tax += over_threshold * AFTER_THRESHOLD_TAX
        return round_cents(tax)

    def tax_owed(self):
        tax_owed = self.tax()
        tax_owed -= self.tax_reduction
        tax_owed -= self.tax_free_amount()
        tax_owed -= self.tax_prepayment
        if 0 > tax_owed:
            tax_owed = Decimal('0')
        return tax_owed

    def tax_owed_rounded(self):
        return round_whole(self.tax_owed())
