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

    def test_significant_digit_printer(self):
        self.assertEqual(r"$12.34 \pm 1.23$", get_rounded_to_significant_digit(x = 1.23456789e1, error = 1.23456789, sig_digit_index = 2))
        self.assertEqual(r"$(1.2 \pm 0.1) \times 10^1$", get_rounded_to_significant_digit(x = 1.23456789e1, error = 1.2345678, sig_digit_index = None))
        self.assertEqual(r"$0.1 \pm 12.3$", get_rounded_to_significant_digit(x = 1.23456789e-1, error = 1.2345678e1, sig_digit_index = 2))
        self.assertEqual(r"$(0 \pm 1) \times 10^1$", get_rounded_to_significant_digit(x = 1.23456789e-2, error = 1.2345678e1, sig_digit_index = None))
        self.assertEqual(r"$0.00012 \pm 0.00001$", get_rounded_to_significant_digit(x = 1.23456789e-3, error = 1.23456789e-4, sig_digit_index = 5))
        self.assertEqual(r"$(1.2 \pm 0.1) times 10^-3$", get_rounded_to_significant_digit(x = 1.23456789e-3, error = 1.23456789e-4, sig_digit_index = None))
        self.assertEqual(r"$1200 \pm 0$", get_rounded_to_significant_digit(x = 1.23456789e3, error = 1.23456789, sig_digit_index = -2))
        self.assertEqual(r"$1234 \pm 1$", get_rounded_to_significant_digit(x = 1.23456789e3, error = 1.23456789, sig_digit_index = None))

if __name__ == "__main__":
    unittest.main()
