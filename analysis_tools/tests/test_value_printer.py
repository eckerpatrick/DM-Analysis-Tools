import unittest

from analysis_tools.value_printer import significant_digit_index, get_rounded_to_significant_digit


class ValuePrinterTests(unittest.TestCase):
    def test_significant_digit_index_for_values_smaller_than_1(self):
        self.assertEqual(significant_digit_index(x=0.01), 3)
        self.assertEqual(significant_digit_index(x=0.03), 2)
        self.assertEqual(significant_digit_index(x=0.0001), 5)
        self.assertEqual(significant_digit_index(x=0.00012345), 5)
        self.assertEqual(significant_digit_index(x=0.00032345), 4)

    def test_significant_digit_index_for_values_greater_than_1(self):
        self.assertEqual(significant_digit_index(x=10), 0)
        self.assertEqual(significant_digit_index(x=123), -1)
        self.assertEqual(significant_digit_index(x=1), 1)
        self.assertEqual(significant_digit_index(x=567), -2)

    def test_significant_digit_index_for_scientific_notation(self):
        self.assertEqual(significant_digit_index(x=1e4), -3)
        self.assertEqual(significant_digit_index(x=1e-4), 5)

    def test_rounding(self):
        self.assertEqual(round(0.123, significant_digit_index(x=0.123)), 0.12)
        self.assertEqual(round(0.323, significant_digit_index(x=0.323)), 0.3)

    def test_significant_digit_printer_without_digit_index(self):
        
        self.assertEqual(r"$12.3 \pm 1.3$", get_rounded_to_significant_digit(x = 1.23456789e1, error = 1.23456789, sig_digit_index = None))   # should this not be error = 13?
        self.assertEqual(r"$(12.3 \pm 1.3) \times 10^{-4}$", get_rounded_to_significant_digit(x = 1.23456789e-3, error = 1.23456789e-4, sig_digit_index = None))
        self.assertEqual(r"$(0.0 \pm 1.3) \times 10^{1}$", get_rounded_to_significant_digit(x = 1.23456789e-2, error = 1.2345678e1, sig_digit_index = None))
        self.assertEqual(r"$1234.6 \pm 1.3$", get_rounded_to_significant_digit(x = 1.23456789e3, error = 1.23456789, sig_digit_index = None))

        self.assertEqual(r"$57 \pm 6$", get_rounded_to_significant_digit(x = 5.6789e1, error = 5.6789, sig_digit_index = None))
        self.assertEqual(r"$(5.7 \pm 0.6) \times 10^{-3}$", get_rounded_to_significant_digit(x = 5.6789e-3, error = 5.6789e-4, sig_digit_index = None))
        self.assertEqual(r"$(1 \pm 6) \times 10^{4}$", get_rounded_to_significant_digit(x = 5.6789e3, error = 5.6789e4, sig_digit_index = None))
        self.assertEqual(r"$(0 \pm 6) \times 10^{1}$", get_rounded_to_significant_digit(x = 5.6789e-2, error = 5.678e1, sig_digit_index = None))
        self.assertEqual(r"$5679 \pm 6$", get_rounded_to_significant_digit(x = 5.6789e3, error = 5.6789, sig_digit_index = None))

    def test_significant_digit_printer_with_digit_index(self):
        self.assertEqual(r"$12.35 \pm 1.24$", get_rounded_to_significant_digit(x = 1.23456789e1, error = 1.23456789, sig_digit_index = 2))
        self.assertEqual(r"$(1.2 \pm 0.1) \times 10^-5$", get_rounded_to_significant_digit(x = 1.23456789e-3, error = 1.23456789e-4, sig_digit_index = 5))
        self.assertEqual(r"$(12 \pm 1235) \times 10^-2$", get_rounded_to_significant_digit(x = 1.23456789e-1, error = 1.2345678e1, sig_digit_index = 2))
        self.assertEqual(r"$1200 \pm 0$", get_rounded_to_significant_digit(x = 1.23456789e3, error = 1.23456789, sig_digit_index = -2))

        # TODO !
        self.assertEqual(r"$57 \pm 6$", get_rounded_to_significant_digit(x = 5.6789e1, error = 5.6789, sig_digit_index = 2))
        self.assertEqual(r"$(5.7 \pm 0.6) \times 10^{-3}$", get_rounded_to_significant_digit(x = 5.6789e-3, error = 5.6789e-4, sig_digit_index = 5))
        self.assertEqual(r"$(0 \pm 6) \times 10^{1}$", get_rounded_to_significant_digit(x = 5.6789e-2, error = 5.678e1, sig_digit_index = 2))
        self.assertEqual(r"$5679 \pm 6$", get_rounded_to_significant_digit(x = 5.6789e3, error = 5.6789, sig_digit_index = 2))

if __name__ == "__main__":
    unittest.main()
