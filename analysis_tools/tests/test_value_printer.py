import unittest

from analysis_tools.value_printer import significant_digit_index


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


if __name__ == "__main__":
    unittest.main()
