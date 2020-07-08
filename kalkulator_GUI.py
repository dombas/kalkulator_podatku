"""
Author: Dominik Dąbek
"""
import json
import re
import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font
import decimal as dec
from typing import Dict, List, Callable
from skala_podatkowa import TaxPeriod

SAVE_FILENAME = 'podatek_dane.txt'


class FormField:
    def __init__(self, label_text: 'str', parent: 'tk.Frame', options: 'GUIOptions', starting_value: 'str' = ''):
        self._label = tk.Label(parent, text=label_text, font=options.default_font())
        self._entry_text = tk.StringVar(value=starting_value)
        self._entry = tk.Entry(parent, textvariable=self._entry_text, font=options.default_font())
        self._default_background = self._entry.cget('background')
        self._options = options

    def entry(self) -> 'tk.Entry':
        return self._entry

    def label(self) -> 'tk.Label':
        return self._label

    def get_input(self) -> 'str':
        return self._entry.get()

    def set_text(self, text_to_set: 'str'):
        self._entry_text.set(text_to_set)

    def attach_write_callback(self, callback: 'Callable'):
        self._entry_text.trace('w', callback)

    def grid(self, row: 'int'):
        self._label.grid(column=0, row=row)
        self._entry.grid(column=1, row=row, sticky='we')

    def set_error(self):
        self._entry.config(background=self._options.error_background)

    def clear_error(self):
        self._entry.config(background=self._default_background)


class OutputFormField(FormField):
    def __init__(self, label_text: 'str', parent: 'tk.Frame', options: 'GUIOptions'):
        super().__init__(label_text, parent, options)
        self._entry.config(state='readonly')


class GUIOptions:
    def __init__(self):
        self.font_size = 14
        self.header_font_size = 16
        self.tab_font_size = 19
        self.error_background = 'salmon'

        self._default_font = tk_font.Font(size=self.font_size)
        self._header_font = tk_font.Font(family='Helvetica', size=self.header_font_size)
        self._tab_font = tk_font.Font(family='Helvetica', size=self.tab_font_size)

        self._style = ttk.Style()
        self._style.configure('TLabelframe.Label', font=self.header_font(), foreground='gray')
        self._style.configure('TNotebook.Tab', font=self.tab_font())

    def default_font(self) -> 'tk_font.Font':
        return self._default_font

    def header_font(self) -> 'tk_font.Font':
        return self._header_font

    def tab_font(self) -> 'tk_font.Font':
        return self._tab_font


def strip_non_numeric(input_str: 'str') -> 'str':
    return re.match(r'^\D*(\d.*\d)\D*$', input_str).group(1)


def only_numeric(input_str: 'str') -> 'str':
    return re.sub(r'\D', '', input_str)


def clean_input(input_str: 'str') -> 'str':
    cleaned_input = strip_non_numeric(input_str)
    separator_index = None
    try:
        if not cleaned_input[-2].isnumeric():
            separator_index = -2
        elif not cleaned_input[-3].isnumeric():
            separator_index = -3
    except IndexError:
        pass
    if separator_index:
        whole_part = only_numeric(cleaned_input[:separator_index])
        fraction_part = only_numeric(cleaned_input[separator_index + 1:])
        cleaned_input = whole_part + '.' + fraction_part
    else:
        cleaned_input = only_numeric(cleaned_input)
    return cleaned_input


def convert_input(input_value: 'str') -> 'dec.Decimal':
    try:
        decimal = dec.Decimal(input_value.replace(',', '.'))
    except (AttributeError, dec.InvalidOperation):
        cleaned_input = clean_input(input_value)
        decimal = dec.Decimal(cleaned_input)
    return decimal


def save_inputs(inputs_dict):
    # TODO error handling
    with open(SAVE_FILENAME, 'w') as file:
        json.dump(inputs_dict, file)


def load_inputs() -> 'Dict[str,str]':
    # TODO error handling
    with open(SAVE_FILENAME, 'r') as file:
        inputs_dict = json.load(file)
    return inputs_dict


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

    MAIN_TAB_TEXT = 'ZALICZKA'
    OPTIONS_TAB_TEXT = 'OPCJE'

    _root: 'tk.Tk'
    _inputs: 'Dict[str,FormField]'
    _outputs: 'Dict[str,OutputFormField]'
    _tax_period: 'TaxPeriod'
    _options: 'GUIOptions'
    _inputs_frame: 'ttk.LabelFrame'
    _outputs_frame: 'ttk.LabelFrame'
    _notebook: 'ttk.Notebook'
    _main_tab: 'tk.Frame'
    _options_tab: 'tk.Frame'

    def __init__(self):
        def create_inputs(parent):
            for input_name, label_text in zip(
                    KalkulatorGUI.INPUT_NAMES,
                    KalkulatorGUI.INPUT_LABELS
            ):
                self._inputs[input_name] = FormField(
                    label_text, parent, self._options)

        def create_outputs(parent):
            for output_name, output_label in zip(
                    KalkulatorGUI.OUTPUT_NAMES,
                    KalkulatorGUI.OUTPUT_LABELS
            ):
                self._outputs[output_name] = OutputFormField(
                    output_label, parent, self._options)

        def create_frames(parent):
            self._inputs_frame = ttk.Labelframe(parent, text=KalkulatorGUI.INPUTS_HEADER)
            self._outputs_frame = ttk.Labelframe(parent, text=KalkulatorGUI.OUTPUTS_HEADER)

        def create_notebook(parent):
            self._notebook = ttk.Notebook(parent)

        def create_tabs(parent):
            self._main_tab = tk.Frame(parent)
            self._options_tab = tk.Frame(parent)

        self._root = tk.Tk()
        self._inputs = {}
        self._outputs = {}
        self._tax_period = TaxPeriod()
        self._options = GUIOptions()

        create_notebook(parent=self._root)
        create_tabs(parent=self._notebook)
        create_frames(parent=self._main_tab)
        create_inputs(parent=self._inputs_frame)
        create_outputs(parent=self._outputs_frame)

    def _arrange_form(self):
        self._main_tab.columnconfigure(0, weight=1)
        self._main_tab.rowconfigure(0, weight=1)
        self._main_tab.rowconfigure(1, weight=1)

        self._notebook.pack(fill='both', expand=1)
        self._main_tab.pack(fill='both', expand=1)
        self._options_tab.pack(fill='both', expand=1)

        self._notebook.add(self._main_tab, text=KalkulatorGUI.MAIN_TAB_TEXT)
        self._notebook.add(self._options_tab, text=KalkulatorGUI.OPTIONS_TAB_TEXT)

        self._inputs_frame.grid(column=0, row=0, sticky='new')
        self._inputs_frame.columnconfigure(1, weight=1)
        current_row = 0
        for input_field in self._all_inputs():
            input_field.grid(current_row)
            current_row += 1

        self._outputs_frame.grid(column=0, row=1, sticky='new')
        self._outputs_frame.columnconfigure(1, weight=1)
        current_row = 0
        for output_field in self._all_outputs():
            output_field.grid(current_row)
            output_field.set_text("read only " + str(current_row))
            current_row += 1

    def _assign_callbacks(self):
        for input_field in self._all_inputs():
            input_field.attach_write_callback(self._update_callback)
        self._root.protocol("WM_DELETE_WINDOW", self._on_closing)

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
        try:
            self._inputs[input_name].clear_error()
            return convert_input(self._inputs[input_name].get_input())
        except (dec.InvalidOperation, AttributeError):
            self._inputs[input_name].set_error()
            return dec.Decimal('0')

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

    def _load_inputs(self):
        try:
            inputs_dict = load_inputs()
            for input_name, value in inputs_dict.items():
                self._inputs[input_name].set_text(value)
        except json.decoder.JSONDecodeError:
            pass

    def _save_inputs(self):
        inputs_dict = {}
        for input_name, value in self._inputs.items():
            inputs_dict[input_name] = value.get_input()
        save_inputs(inputs_dict)

    def _on_closing(self):
        # TODO error handling
        self._save_inputs()
        self._root.destroy()

    def main_loop(self):
        self._arrange_form()
        self._assign_callbacks()
        self._update_callback()
        self._load_inputs()
        self._root.mainloop()


def main():
    kalkulator_gui = KalkulatorGUI()
    kalkulator_gui.main_loop()


if __name__ == "__main__":
    main()
