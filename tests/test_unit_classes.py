"""Unit tests for Meal, Menu, and UserPreferences classes."""

import unittest
from information_retreival_MealClass import Meal
from information_retreival_MenuClass import Menu
from information_retreival_UserPreferences import UserPreferences


class TestMealClass(unittest.TestCase):
    """Test Meal class methods."""

    def test_meal_creation(self):
        """Test creating a meal."""
        meal = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        self.assertEqual(meal.id, "1")
        self.assertEqual(meal.name, "Pasta")
        self.assertEqual(meal.price, 12.5)

    def test_add_rating(self):
        """Test adding ratings to meal."""
        meal = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        meal.add_rating(5)
        meal.add_rating(4)
        self.assertEqual(meal.average_rating, 4.5)

    def test_to_dict(self):
        """Test converting meal to dictionary."""
        meal = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        meal_dict = meal.to_dict()
        self.assertEqual(meal_dict["name"], "Pasta")
        self.assertEqual(meal_dict["price"], 12.5)


class TestMenuClass(unittest.TestCase):
    """Test Menu class methods."""

    def test_menu_creation(self):
        """Test creating empty menu."""
        menu = Menu()
        self.assertEqual(len(menu), 0)

    def test_add_meal(self):
        """Test adding meal to menu."""
        menu = Menu()
        meal = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        menu.add(meal)
        self.assertEqual(len(menu), 1)

    def test_get_meal(self):
        """Test retrieving meal by ID."""
        menu = Menu()
        meal = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        menu.add(meal)
        retrieved = menu.get("1")
        self.assertEqual(retrieved.name, "Pasta")

    def test_filter_by_diet(self):
        """Test filtering meals by diet."""
        menu = Menu()
        m1 = Meal("1", "Salad", 8.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Burger", 10.0, 500, "meat", "savory")
        menu.add(m1)
        menu.add(m2)
        
        veg_meals = menu.filter_by_diet("vegetarian")
        self.assertEqual(len(veg_meals), 1)
        self.assertEqual(veg_meals[0].name, "Salad")

    def test_filter_by_price(self):
        """Test filtering meals by price."""
        menu = Menu()
        m1 = Meal("1", "Salad", 8.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Steak", 25.0, 700, "meat", "rich")
        menu.add(m1)
        menu.add(m2)
        
        affordable = menu.filter_by_price(10.0)
        self.assertEqual(len(affordable), 1)
        self.assertEqual(affordable[0].name, "Salad")

    def test_average_price(self):
        """Test calculating average price."""
        menu = Menu()
        m1 = Meal("1", "Salad", 10.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Pasta", 20.0, 600, "vegetarian", "savory")
        menu.add(m1)
        menu.add(m2)
        
        avg = menu.average_price()
        self.assertEqual(avg, 15.0)


class TestUserPreferencesClass(unittest.TestCase):
    """Test UserPreferences class methods."""

    def test_preferences_creation(self):
        """Test creating user preferences."""
        prefs = UserPreferences(history_ids=["1", "2"], budget=15.0)
        self.assertEqual(len(prefs.history_ids), 2)
        self.assertEqual(prefs.budget, 15.0)

    def test_add_meal_to_history(self):
        """Test adding meal to history."""
        prefs = UserPreferences()
        prefs.add_meal_to_history("1")
        prefs.add_meal_to_history("2")
        self.assertEqual(len(prefs.history_ids), 2)

    def test_check_budget(self):
        """Test budget checking."""
        prefs = UserPreferences(budget=15.0)
        self.assertTrue(prefs.check_budget(10.0))
        self.assertFalse(prefs.check_budget(20.0))

    def test_update_preferences(self):
        """Test preference learning."""
        meals = [
            {"id": "1", "flavor": "spicy", "diet": "vegetarian"},
            {"id": "2", "flavor": "mild", "diet": "meat"}
        ]
        prefs = UserPreferences(history_ids=["1", "1"])
        prefs.update_preferences(meals)
        
        weights = prefs.token_weights
        self.assertIn("spicy", weights)
        self.assertIn("vegetarian", weights)


if __name__ == "__main__":
    unittest.main()
