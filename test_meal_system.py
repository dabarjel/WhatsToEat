"""Tests for meal recommendation system."""

import unittest
from meal_items import AbstractMealItem, StandardMeal, SpecialtyMeal, BundleMeal
from menu import Menu
from recommendations import Recommendations


class TestInheritance(unittest.TestCase):
    """Test inheritance hierarchy."""

    def test_cannot_instantiate_abstract_class(self):
        """AbstractMealItem cannot be instantiated."""
        with self.assertRaises(TypeError):
            AbstractMealItem("1", "Test", 10.0, 500, "veg", "mild")

    def test_standard_meal_is_abstract_meal(self):
        """StandardMeal is instance of AbstractMealItem."""
        meal = StandardMeal("1", "Pasta", 12.0, 600, "vegetarian", "savory")
        self.assertIsInstance(meal, AbstractMealItem)

    def test_specialty_meal_is_abstract_meal(self):
        """SpecialtyMeal is instance of AbstractMealItem."""
        meal = SpecialtyMeal("2", "Risotto", 25.0, 550, "vegetarian", "rich")
        self.assertIsInstance(meal, AbstractMealItem)

    def test_bundle_meal_is_abstract_meal(self):
        """BundleMeal is instance of AbstractMealItem."""
        meal = BundleMeal("3", "Combo", 20.0, 1200, "mixed", "varied")
        self.assertIsInstance(meal, AbstractMealItem)


class TestPolymorphism(unittest.TestCase):
    """Test polymorphic behavior."""

    def test_different_value_calculations(self):
        """Different meal types calculate value differently."""
        standard = StandardMeal("1", "Meal1", 10.0, 500, "veg", "mild")
        specialty = SpecialtyMeal("2", "Meal2", 10.0, 500, "veg", "mild")
        bundle = BundleMeal("3", "Meal3", 10.0, 500, "mixed", "varied")

        for meal in [standard, specialty, bundle]:
            meal.add_rating(4)

        v1 = standard.calculate_value_score()
        v2 = specialty.calculate_value_score()
        v3 = bundle.calculate_value_score()

        self.assertNotEqual(v1, v2)
        self.assertNotEqual(v2, v3)

    def test_different_preparation_info(self):
        """Different meal types return different prep info."""
        standard = StandardMeal("1", "Meal1", 10.0, 500, "veg", "mild")
        specialty = SpecialtyMeal("2", "Meal2", 15.0, 550, "veg", "spicy", 40)
        bundle = BundleMeal("3", "Meal3", 20.0, 1000, "mixed", "varied")

        info1 = standard.get_preparation_info()
        info2 = specialty.get_preparation_info()
        info3 = bundle.get_preparation_info()

        self.assertNotEqual(info1, info2)
        self.assertNotEqual(info2, info3)
        self.assertIn("Standard", info1)
        self.assertIn("40", info2)
        self.assertIn("Bundle", info3)


class TestComposition(unittest.TestCase):
    """Test composition relationships."""

    def test_menu_contains_meals(self):
        """Menu has-a collection of meals."""
        menu = Menu()
        meal1 = StandardMeal("1", "Pasta", 12.0, 600, "vegetarian", "savory")
        meal2 = SpecialtyMeal("2", "Steak", 30.0, 700, "meat", "rich")

        menu.add_meal(meal1)
        menu.add_meal(meal2)

        self.assertEqual(len(menu), 2)
        self.assertEqual(menu.get_meal("1").name, "Pasta")

    def test_recommendations_has_menu(self):
        """Recommendations has-a menu."""
        menu = Menu()
        rec = Recommendations(menu)

        self.assertIsInstance(rec._menu, Menu)

    def test_menu_works_with_mixed_types(self):
        """Menu works polymorphically with different meal types."""
        menu = Menu()
        menu.add_meal(StandardMeal("1", "Meal1", 10.0, 500, "veg", "mild"))
        menu.add_meal(SpecialtyMeal("2", "Meal2", 20.0, 600, "veg", "spicy"))
        menu.add_meal(BundleMeal("3", "Meal3", 15.0, 1000, "mixed", "varied"))

        scores = menu.get_value_scores()
        self.assertEqual(len(scores), 3)
        self.assertIn("1", scores)
        self.assertIn("2", scores)
        self.assertIn("3", scores)


class TestSystemIntegration(unittest.TestCase):
    """Test complete system."""

    def test_complete_workflow(self):
        """Test full recommendation workflow."""
        menu = Menu()

        meal1 = StandardMeal("1", "Salad", 8.0, 300, "vegetarian", "fresh")
        meal1.add_rating(4)
        meal2 = SpecialtyMeal("2", "Steak", 35.0, 800, "meat", "rich", 45)
        meal2.add_rating(5)

        menu.add_meal(meal1)
        menu.add_meal(meal2)

        rec = Recommendations(menu)
        rec.add_to_history("1")

        suggestions = rec.recommend_by_value(top_k=2)

        self.assertEqual(len(suggestions), 2)
        self.assertIsInstance(suggestions[0], AbstractMealItem)


if __name__ == '__main__':
    unittest.main()
