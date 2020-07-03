"""
Author: Dominik Dąbek
"""

import tkinter as tk
import tkinter.font as tk_font
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

    def apply_options(self, gui_options: 'GUIOptions'):
        self._entry.config(font=gui_options.default_font())
        self._label.config(font=gui_options.default_font())


class OutputFormField(FormField):
    def __init__(self, label_text, root):
        super().__init__(label_text, root)
        self._entry.config(state='readonly')

    def set_text(self, text_to_set):
        self._entry_text.set(text_to_set)


class GUIOptions:
    def __init__(self):
        self.font_size = 14
        self.header_font_size = 20

    def default_font(self):
        return tk_font.Font(size=self.font_size)

    def header_font(self):
        return tk_font.Font(size=self.header_font_size)


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
    options: 'GUIOptions'
    inputs_header: 'tk.Label'
    outputs_header: 'tk.Label'

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

        def create_headers():
            self.inputs_header = tk.Label(self.root, text=KalkulatorGUI.INPUTS_HEADER)
            self.outputs_header = tk.Label(self.root, text=KalkulatorGUI.OUTPUTS_HEADER)

        self.root = tk.Tk()
        self.inputs = {}
        self.outputs = {}
        self.tax_period = TaxPeriod()
        self.options = GUIOptions()

        create_inputs()
        create_outputs()
        create_headers()

    def arrange_form(self):
        # FIXME remove code duplication
        current_row = 0
        self.inputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for input_name in KalkulatorGUI.INPUT_NAMES:
            input_field = self.inputs[input_name]
            input_field.label().grid(column=0, row=current_row)
            input_field.entry().grid(column=1, row=current_row)
            current_row += 1

        self.outputs_header.grid(column=0, row=current_row, columnspan=2)
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

    def all_form_fields(self):
        return self.all_inputs() + self.all_outputs()

    def all_outputs(self):
        _all_outputs = []
        for output_name in KalkulatorGUI.OUTPUT_NAMES:
            _all_outputs.append(self.outputs[output_name])
        return _all_outputs

    def all_inputs(self):
        _all_inputs = []
        for input_name in KalkulatorGUI.INPUT_NAMES:
            _all_inputs.append(self.inputs[input_name])
        return _all_inputs

    def apply_options(self):
        for form_field in self.all_form_fields():
            form_field.apply_options(self.options)
        self.inputs_header.config(font=self.options.header_font())
        self.outputs_header.config(font=self.options.header_font())

    def main_loop(self):
        self.arrange_form()
        self.assign_callbacks()
        self.apply_options()
        self.root.mainloop()


def main():
    kalkulator_gui = KalkulatorGUI()
    kalkulator_gui.main_loop()


if __name__ == "__main__":
    main()
