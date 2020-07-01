"""
Author: Dominik Dąbek
"""

import tkinter as tk
import decimal as dec
from typing import Dict

from skala_podatkowa import TaxPeriod


class FormField:
    def __init__(self, label_text, root):
        self._label = tk.Label(root, text=label_text)
        self._entry_text = tk.StringVar()
        self._entry = tk.Entry(root, textvariable=self._entry_text)

    def entry(self):
        return self._entry

    def label(self):
        return self._label

    def get_input(self) -> 'str':
        return self._entry.get()

    def attach_write_callback(self, callback):
        print("attaching callback")
        self._entry_text.trace('w', callback)


class OutputFormField(FormField):
    def __init__(self, label_text, root):
        super().__init__(label_text, root)
        self._entry.config(state='readonly')

    def set_text(self, text_to_set):
        self._entry_text.set(text_to_set)


class KalkulatorGUI:
    INPUT_NAMES = [
        'revenue',
        'expenses',
        'tax_reduction',
        'income_reduction',
        'tax_prepayment']

    INPUT_LABELS = [
        'Przychód',
        'Koszty',
        'Odliczenia od podatku',
        'Odliczenia od dochodu',
        'Zapłacone zaliczki'
    ]

    INPUTS_HEADER = 'Do wprowadzenia'

    OUTPUT_NAMES = [
        'income',
        'tax_basis',
        'tax',
        'tax_owed'
    ]

    OUTPUT_LABELS = [
        'Dochód',
        'Podstawa obliczenia podatku',
        'Podatek według skali',
        'Zaliczka do zapłaty'
    ]

    OUTPUTS_HEADER = 'Wyliczenia'

    inputs: 'Dict[str,FormField]'
    outputs: 'Dict[str,OutputFormField]'
    tax_period: 'TaxPeriod'

    def __init__(self):
        def create_inputs():
            for input_name, input_label in zip(
                    KalkulatorGUI.INPUT_NAMES,
                    KalkulatorGUI.INPUT_LABELS
            ):
                self.inputs[input_name] = FormField(input_label, self.root)

        def create_outputs():
            for output_name, output_label in zip(
                    KalkulatorGUI.OUTPUT_NAMES,
                    KalkulatorGUI.OUTPUT_LABELS
            ):
                self.outputs[output_name] = OutputFormField(output_label, self.root)

        self.root = tk.Tk()
        self.inputs = {}
        self.outputs = {}
        self.tax_period = TaxPeriod()

        create_inputs()
        create_outputs()

    def arrange_form(self):
        # FIXME remove code duplication
        current_row = 0

        inputs_header = tk.Label(self.root, text=KalkulatorGUI.INPUTS_HEADER)
        inputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for input_name in KalkulatorGUI.INPUT_NAMES:
            input_field = self.inputs[input_name]
            input_field.label().grid(column=0, row=current_row)
            input_field.entry().grid(column=1, row=current_row)
            current_row += 1

        outputs_header = tk.Label(self.root, text=KalkulatorGUI.OUTPUTS_HEADER)
        outputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for output_name in KalkulatorGUI.OUTPUT_NAMES:
            output_field = self.outputs[output_name]
            output_field.label().grid(column=0, row=current_row)
            output_field.entry().grid(column=1, row=current_row)
            output_field.set_text("read only " + str(current_row))
            current_row += 1

    def assign_callbacks(self):
        print("assigning callbacks")
        for input_name in KalkulatorGUI.INPUT_NAMES:
            self.inputs[input_name].attach_write_callback(self.update_callback)

    def update_callback(self, *args):
        print("running update callback")
        self.update_tax_period_from_inputs()
        self.update_outputs()

    def update_outputs(self):
        self.outputs['income'].set_text(
            self.tax_period.income()
        )
        self.outputs['tax_basis'].set_text(
            self.tax_period.tax_basis()
        )
        self.outputs['tax'].set_text(
            self.tax_period.tax()
        )
        self.outputs['tax_owed'].set_text(
            self.tax_period.tax_owed()
        )

    def update_tax_period_from_inputs(self):
        try:
            self.tax_period.set_revenue(
                dec.Decimal(self.read_input('revenue'))
            )
        except dec.InvalidOperation:
            self.tax_period.set_revenue(
                dec.Decimal('0')
            )

        try:
            self.tax_period.set_expenses(
                dec.Decimal(self.read_input('expenses'))
            )
        except dec.InvalidOperation:
            self.tax_period.set_expenses(
                dec.Decimal('0')
            )

        try:
            self.tax_period.set_tax_reduction(
                dec.Decimal(self.read_input('tax_reduction'))
            )
        except dec.InvalidOperation:
            self.tax_period.set_tax_reduction(
                dec.Decimal('0')
            )

        try:
            self.tax_period.set_income_reduction(
                dec.Decimal(self.read_input('income_reduction'))
            )
        except dec.InvalidOperation:
            self.tax_period.set_income_reduction(
                dec.Decimal('0')
            )

        try:
            self.tax_period.set_tax_prepayment(
                dec.Decimal(self.read_input('tax_prepayment'))
            )
        except dec.InvalidOperation:
            self.tax_period.set_tax_prepayment(
                dec.Decimal('0')
            )

    def read_input(self, input_name):
        return self.inputs[input_name].get_input().replace(',', '.')

    def main_loop(self):
        self.arrange_form()
        self.assign_callbacks()
        self.root.mainloop()


def main():
    kalkulator_gui = KalkulatorGUI()
    kalkulator_gui.main_loop()


if __name__ == "__main__":
    main()
