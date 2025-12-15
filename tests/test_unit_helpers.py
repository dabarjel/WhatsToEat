import unittest
from meal_finder_library import normalize_text, within_budget, average_price


class TestHelperFunctions(unittest.TestCase):

    def test_normalize_text_basic(self):
        self.assertEqual(normalize_text("  Hello World "), "hello world")

    def test_normalize_text_multiple_spaces(self):
        self.assertEqual(normalize_text("Hello    World"), "hello world")

    def test_within_budget_true(self):
        meal = {"price": 10}
        self.assertTrue(within_budget(meal, 15))

    def test_within_budget_false(self):
        meal = {"price": 20}
        self.assertFalse(within_budget(meal, 15))

    def test_average_price(self):
        meals = [
            {"price": 10},
            {"price": 20},
            {"price": 30}
        ]
        self.assertEqual(average_price(meals), 20)


if __name__ == "__main__":
    un
