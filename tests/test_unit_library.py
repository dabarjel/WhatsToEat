"""Unit tests for meal_finder_library functions."""

import unittest
from meal_finder_library import (
    normalize_text,
    within_budget,
    format_meal,
    average_price,
    count_vegetarian,
    parse_menu_csv,
    filter_by_diet,
    filter_by_price,
    add_rating,
    get_average_rating
)


class TestSimpleFunctions(unittest.TestCase):
    """Test simple helper functions."""

    def test_normalize_text_basic(self):
        """Test basic text normalization."""
        result = normalize_text("  Hello World ")
        self.assertEqual(result, "hello world")

    def test_normalize_text_multiple_spaces(self):
        """Test collapsing multiple spaces."""
        result = normalize_text("Hello    World")
        self.assertEqual(result, "hello world")

    def test_within_budget_true(self):
        """Test price within budget."""
        self.assertTrue(within_budget(10.0, 15.0))

    def test_within_budget_false(self):
        """Test price over budget."""
        self.assertFalse(within_budget(20.0, 15.0))

    def test_format_meal(self):
        """Test meal formatting."""
        meal = {"id": "1", "name": "Pasta", "price": 12.5, "calories": 600}
        result = format_meal(meal)
        self.assertIn("Pasta", result)
        self.assertIn("12.50", result)

    def test_average_price(self):
        """Test average price calculation."""
        meals = [
            {"price": 10.0},
            {"price": 20.0},
            {"price": 30.0}
        ]
        result = average_price(meals)
        self.assertEqual(result, 20.0)

    def test_count_vegetarian(self):
        """Test counting vegetarian meals."""
        meals = [
            {"diet": "vegetarian"},
            {"diet": "meat"},
            {"diet": "vegetarian"}
        ]
        result = count_vegetarian(meals)
        self.assertEqual(result, 2)


class TestMediumFunctions(unittest.TestCase):
    """Test medium complexity functions."""

    def test_parse_menu_csv(self):
        """Test CSV parsing."""
        csv_text = "id,name,price,calories,diet,flavor\n1,Burger,10.0,500,meat,savory"
        meals = parse_menu_csv(csv_text)
        self.assertEqual(len(meals), 1)
        self.assertEqual(meals[0]["name"], "Burger")

    def test_filter_by_diet(self):
        """Test diet filtering."""
        meals = [
            {"id": "1", "name": "Salad", "diet": "vegetarian", "price": 8.0},
            {"id": "2", "name": "Burger", "diet": "meat", "price": 10.0}
        ]
        result = filter_by_diet(meals, "vegetarian")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Salad")

    def test_filter_by_price(self):
        """Test price filtering."""
        meals = [
            {"id": "1", "name": "Salad", "price": 8.0},
            {"id": "2", "name": "Steak", "price": 25.0}
        ]
        result = filter_by_price(meals, 10.0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Salad")

    def test_add_rating(self):
        """Test adding ratings to a meal."""
        meal = {"id": "1", "name": "Pasta", "price": 12.0, "ratings": []}
        add_rating(meal, 5)
        add_rating(meal, 4)
        self.assertEqual(len(meal["ratings"]), 2)
        self.assertIn(5, meal["ratings"])

    def test_get_average_rating(self):
        """Test average rating calculation."""
        meal = {"ratings": [5, 4, 3]}
        result = get_average_rating(meal)
        self.assertEqual(result, 4.0)

    def test_get_average_rating_no_ratings(self):
        """Test average rating with no ratings."""
        meal = {"ratings": []}
        result = get_average_rating(meal)
        self.assertEqual(result, 0.0)


if __name__ == "__main__":
    unittest.main()
