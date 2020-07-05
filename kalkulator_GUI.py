"""
Author: Dominik Dąbek
"""
import re
import tkinter as tk
import tkinter.font as tk_font
import decimal as dec
from typing import Dict, List, Callable

from skala_podatkowa import TaxPeriod


class FormField:
    def __init__(self, label_text: 'str', root: 'tk.Tk', starting_value: 'str' = ''):
        self._label = tk.Label(root, text=label_text)
        self._entry_text = tk.StringVar(value=starting_value)
        self._entry = tk.Entry(root, textvariable=self._entry_text)

    def entry(self) -> 'tk.Entry':
        return self._entry

    def label(self) -> 'tk.Label':
        return self._label

    def get_input(self) -> 'str':
        return self._entry.get()

    def attach_write_callback(self, callback: 'Callable'):
        self._entry_text.trace('w', callback)

    def apply_options(self, gui_options: 'GUIOptions'):
        self._entry.config(font=gui_options.default_font())
        self._label.config(font=gui_options.default_font())

    def grid(self, row: 'int'):
        self._label.grid(column=0, row=row)
        self._entry.grid(column=1, row=row)


class OutputFormField(FormField):
    def __init__(self, label_text: 'str', root: 'tk.Tk'):
        super().__init__(label_text, root)
        self._entry.config(state='readonly')

    def set_text(self, text_to_set: 'str'):
        self._entry_text.set(text_to_set)


class GUIOptions:
    def __init__(self):
        self.font_size = 14
        self.header_font_size = 20

    def default_font(self) -> 'tk_font.Font':
        return tk_font.Font(size=self.font_size)

    def header_font(self) -> 'tk_font.Font':
        return tk_font.Font(size=self.header_font_size)


def strip_non_numeric(input_str: 'str') -> 'str':
    return re.match(r'^\D*(\d.*\d)\D*$', input_str).group(1)


def only_numeric(input_str: 'str') -> 'str':
    return re.sub(r'\D', '', input_str)


def clean_input(input_str: 'str') -> 'str':
    cleaned_input = strip_non_numeric(input_str)
    separator_index = None
    if not cleaned_input[-2].isnumeric():
        separator_index = -2
    elif not cleaned_input[-3].isnumeric():
        separator_index = -3
    if separator_index:
        whole_part = only_numeric(cleaned_input[:separator_index])
        fraction_part = only_numeric(cleaned_input[separator_index+1:])
        cleaned_input = whole_part+'.'+fraction_part
    else:
        cleaned_input = only_numeric(cleaned_input)
    return cleaned_input


def convert_input(input_value: 'str') -> 'dec.Decimal':
    cleaned_input = clean_input(input_value)
    decimal = dec.Decimal('0')
    try:
        decimal = dec.Decimal(cleaned_input)
    except dec.InvalidOperation:
        print(f'Error reading input \"{input_value}\"')
        # TODO inform user which field is having problems
    finally:
        return decimal


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

    DEFAULT_INPUT_VALUES = [
        '11300,00',
        '1153,73',
        '918,82',
        '652,41',
        '0,00'
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

    _root: 'tk.Tk'
    _inputs: 'Dict[str,FormField]'
    _outputs: 'Dict[str,OutputFormField]'
    _tax_period: 'TaxPeriod'
    _options: 'GUIOptions'
    _inputs_header: 'tk.Label'
    _outputs_header: 'tk.Label'

    def __init__(self):
        def create_inputs():
            for input_name, label_text, starting_value in zip(
                    KalkulatorGUI.INPUT_NAMES,
                    KalkulatorGUI.INPUT_LABELS,
                    KalkulatorGUI.DEFAULT_INPUT_VALUES
            ):
                self._inputs[input_name] = FormField(label_text, self._root, starting_value)

        def create_outputs():
            for output_name, output_label in zip(
                    KalkulatorGUI.OUTPUT_NAMES,
                    KalkulatorGUI.OUTPUT_LABELS
            ):
                self._outputs[output_name] = OutputFormField(output_label, self._root)

        def create_headers():
            self._inputs_header = tk.Label(self._root, text=KalkulatorGUI.INPUTS_HEADER)
            self._outputs_header = tk.Label(self._root, text=KalkulatorGUI.OUTPUTS_HEADER)

        self._root = tk.Tk()
        self._inputs = {}
        self._outputs = {}
        self._tax_period = TaxPeriod()
        self._options = GUIOptions()

        create_inputs()
        create_outputs()
        create_headers()

    def _arrange_form(self):
        current_row = 0
        self._inputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for input_field in self._all_inputs():
            input_field.grid(current_row)
            current_row += 1

        self._outputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for output_field in self._all_outputs():
            output_field.grid(current_row)
            output_field.set_text("read only " + str(current_row))
            current_row += 1

    def _assign_callbacks(self):
        for input_field in self._all_inputs():
            input_field.attach_write_callback(self._update_callback)

    def _update_callback(self, *_):
        self._update_tax_period_from_inputs()
        self._update_outputs()

    def _update_outputs(self):
        self._outputs['income'].set_text(
            str(self._tax_period.income())
        )
        self._outputs['tax_basis'].set_text(
            str(self._tax_period.tax_basis())
        )
        self._outputs['tax'].set_text(
            str(self._tax_period.tax())
        )
        self._outputs['tax_owed'].set_text(
            str(self._tax_period.tax_owed())
        )

    def _update_tax_period_from_inputs(self):
        self._tax_period.set_revenue(
            self._read_input('revenue')
        )

        self._tax_period.set_expenses(
            self._read_input('expenses')
        )

        self._tax_period.set_tax_reduction(
            self._read_input('tax_reduction')
        )

        self._tax_period.set_income_reduction(
            self._read_input('income_reduction')
        )

        self._tax_period.set_tax_prepayment(
            self._read_input('tax_prepayment')
        )

    def _read_input(self, input_name: 'str') -> 'dec.Decimal':
        return convert_input(self._inputs[input_name].get_input())

    def _all_form_fields(self) -> 'List[FormField]':
        return self._all_inputs() + self._all_outputs()

    def _all_outputs(self) -> 'List[OutputFormField]':
        _all_outputs = []
        for output_name in KalkulatorGUI.OUTPUT_NAMES:
            _all_outputs.append(self._outputs[output_name])
        return _all_outputs

    def _all_inputs(self) -> 'List[FormField]':
        _all_inputs = []
        for input_name in KalkulatorGUI.INPUT_NAMES:
            _all_inputs.append(self._inputs[input_name])
        return _all_inputs

    def _apply_options(self):
        for form_field in self._all_form_fields():
            form_field.apply_options(self._options)
        self._inputs_header.config(font=self._options.header_font())
        self._outputs_header.config(font=self._options.header_font())

    def main_loop(self):
        self._arrange_form()
        self._assign_callbacks()
        self._apply_options()
        self._update_callback()
        self._root.mainloop()


def main():
    kalkulator_gui = KalkulatorGUI()
    kalkulator_gui.main_loop()


if __name__ == "__main__":
    main()
