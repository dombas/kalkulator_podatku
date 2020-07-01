"""
Author: Dominik Dąbek
"""

from tkinter import *
from typing import Dict

from skala_podatkowa import TaxPeriod


class FormField:
    def __init__(self, label_text, root):
        self._label = Label(root, text=label_text)
        self._entry = Entry(root)

    def entry(self):
        return self._entry

    def label(self):
        return self._label


class OutputFormField(FormField):
    def __init__(self, label_text, root):
        super().__init__(label_text, root)
        self._entry_text = StringVar()
        self._entry.config(state='readonly', textvariable=self._entry_text)

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
    outputs: 'Dict[str,FormField]'
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

        self.root = Tk()
        self.inputs = {}
        self.outputs = {}
        self.tax_period = TaxPeriod()

        create_inputs()
        create_outputs()

    def arrange_form(self):
        # FIXME remove code duplication
        current_row = 0

        inputs_header = Label(self.root, text=KalkulatorGUI.INPUTS_HEADER)
        inputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for input_name in KalkulatorGUI.INPUT_NAMES:
            input_field = self.inputs[input_name]
            input_field.label().grid(column=0, row=current_row)
            input_field.entry().grid(column=1, row=current_row)
            current_row += 1

        outputs_header = Label(self.root, text=KalkulatorGUI.OUTPUTS_HEADER)
        outputs_header.grid(column=0, row=current_row, columnspan=2)
        current_row += 1

        for output_name in KalkulatorGUI.OUTPUT_NAMES:
            output_field = self.outputs[output_name]
            output_field.label().grid(column=0, row=current_row)
            output_field.entry().grid(column=1, row=current_row)
            output_field.set_text("read only " + str(current_row))
            current_row += 1

    def main_loop(self):
        self.arrange_form()
        self.root.mainloop()


def main():
    kalkulator_gui = KalkulatorGUI()
    kalkulator_gui.main_loop()


if __name__ == "__main__":
    main()
