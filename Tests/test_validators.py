import unittest
from Models.validators import (
    is_positive_number,
    is_non_negative_number,
    is_number_in_range,
    is_non_empty_string,
    is_non_negative_int,
)


class TestIsPositiveNumber(unittest.TestCase):
    def test_positive_int(self):
        self.assertTrue(is_positive_number(5))

    def test_positive_float(self):
        self.assertTrue(is_positive_number(0.001))

    def test_zero_is_false(self):
        self.assertFalse(is_positive_number(0))

    def test_negative_is_false(self):
        self.assertFalse(is_positive_number(-1))

    def test_bool_true_is_false(self):
        self.assertFalse(is_positive_number(True))

    def test_string_is_false(self):
        self.assertFalse(is_positive_number("5"))


class TestIsNonNegativeNumber(unittest.TestCase):
    def test_zero_is_true(self):
        self.assertTrue(is_non_negative_number(0))

    def test_positive_is_true(self):
        self.assertTrue(is_non_negative_number(100.5))

    def test_negative_is_false(self):
        self.assertFalse(is_non_negative_number(-0.01))

    def test_bool_is_false(self):
        self.assertFalse(is_non_negative_number(False))


class TestIsNumberInRange(unittest.TestCase):
    def test_within_range(self):
        self.assertTrue(is_number_in_range(0.5, 0, 1))

    def test_at_lower_bound(self):
        self.assertTrue(is_number_in_range(0, 0, 1))

    def test_at_upper_bound(self):
        self.assertTrue(is_number_in_range(1, 0, 1))

    def test_below_range(self):
        self.assertFalse(is_number_in_range(-0.1, 0, 1))

    def test_above_range(self):
        self.assertFalse(is_number_in_range(1.1, 0, 1))

    def test_bool_is_false(self):
        self.assertFalse(is_number_in_range(True, 0, 1))


class TestIsNonEmptyString(unittest.TestCase):
    def test_valid_string(self):
        self.assertTrue(is_non_empty_string("hello"))

    def test_empty_string_is_false(self):
        self.assertFalse(is_non_empty_string(""))

    def test_integer_is_false(self):
        self.assertFalse(is_non_empty_string(42))

    def test_none_is_false(self):
        self.assertFalse(is_non_empty_string(None))


class TestIsNonNegativeInt(unittest.TestCase):
    def test_zero(self):
        self.assertTrue(is_non_negative_int(0))

    def test_positive_int(self):
        self.assertTrue(is_non_negative_int(10))

    def test_negative_is_false(self):
        self.assertFalse(is_non_negative_int(-1))

    def test_float_is_false(self):
        self.assertFalse(is_non_negative_int(1.0))

    def test_bool_is_false(self):
        self.assertFalse(is_non_negative_int(True))


if __name__ == "__main__":
    unittest.main()
