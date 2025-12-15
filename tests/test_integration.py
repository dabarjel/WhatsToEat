"""Integration tests - testing how components work together."""

import unittest
from information_retreival_MealClass import Meal
from information_retreival_MenuClass import Menu
from information_retreival_UserPreferences import UserPreferences
from meal_finder_library import (
    filter_by_diet,
    filter_by_price,
    recommend_meals,
    learn_preferences_from_history
)


class TestMenuMealIntegration(unittest.TestCase):
    """Test Menu and Meal working together."""

    def test_menu_with_multiple_meals(self):
        """Test menu operations with multiple meals."""
        menu = Menu()
        m1 = Meal("1", "Salad", 8.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Burger", 12.0, 600, "meat", "savory")
        m3 = Meal("3", "Pasta", 10.0, 500, "vegetarian", "creamy")
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        
        # Test filtering
        veg_meals = menu.filter_by_diet("vegetarian")
        self.assertEqual(len(veg_meals), 2)

    def test_csv_to_menu_workflow(self):
        """Test importing CSV data into menu."""
        csv_text = """id,name,price,calories,diet,flavor
1,Salad,8.0,300,vegetarian,fresh
2,Burger,12.0,600,meat,savory"""
        
        menu, errors = Menu.from_csv(csv_text)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(menu), 2)


class TestPreferencesMenuIntegration(unittest.TestCase):
    """Test UserPreferences with Menu."""

    def test_preferences_learn_from_menu(self):
        """Test learning preferences from menu history."""
        menu = Menu()
        m1 = Meal("1", "Spicy Tofu", 9.0, 400, "vegan", "spicy")
        m2 = Meal("2", "Mild Pasta", 11.0, 550, "vegetarian", "mild")
        menu.add(m1)
        menu.add(m2)
        
        prefs = UserPreferences(history_ids=["1", "1", "2"], budget=15.0)
        meal_dicts = [m.to_dict() for m in menu.meals]
        prefs.update_preferences(meal_dicts)
        
        weights = prefs.token_weights
        # Should prefer spicy and vegan more (appears twice)
        self.assertIn("spicy", weights)
        self.assertIn("vegan", weights)


class TestFilteringAndRating(unittest.TestCase):
    """Test filtering combined with ratings."""

    def test_filter_then_rate_workflow(self):
        """Test filtering meals then adding ratings."""
        meals = [
            {"id": "1", "name": "Salad", "diet": "vegetarian", "price": 8.0, "flavor": "fresh", "ratings": []},
            {"id": "2", "name": "Burger", "diet": "meat", "price": 12.0, "flavor": "savory", "ratings": []},
            {"id": "3", "name": "Pasta", "diet": "vegetarian", "price": 10.0, "flavor": "creamy", "ratings": []}
        ]
        
        # Filter by diet
        veg_meals = filter_by_diet(meals, "vegetarian")
        self.assertEqual(len(veg_meals), 2)
        
        # Filter by price
        affordable_veg = filter_by_price(veg_meals, 9.0)
        self.assertEqual(len(affordable_veg), 1)
        self.assertEqual(affordable_veg[0]["name"], "Salad")


class TestRecommendationWorkflow(unittest.TestCase):
    """Test recommendation generation workflow."""

    def test_recommend_with_preferences(self):
        """Test recommendations using learned preferences."""
        meals = [
            {"id": "1", "name": "Spicy Tofu", "price": 9.0, "diet": "vegan", "flavor": "spicy", "ratings": [5, 4]},
            {"id": "2", "name": "Mild Pasta", "price": 11.0, "diet": "vegetarian", "flavor": "mild", "ratings": [3]},
            {"id": "3", "name": "Spicy Curry", "price": 13.0, "diet": "vegan", "flavor": "spicy", "ratings": [5]}
        ]
        
        prefs = {"spicy": 0.5, "vegan": 0.5}
        recommendations = recommend_meals(meals, prefs=prefs, top_k=2, strategy="best")
        
        self.assertEqual(len(recommendations), 2)
        # Higher rated spicy meals should be recommended
        self.assertIn(recommendations[0]["name"], ["Spicy Tofu", "Spicy Curry"])

    def test_recommend_with_budget(self):
        """Test recommendations with budget constraint."""
        meals = [
            {"id": "1", "name": "Salad", "price": 8.0, "diet": "vegetarian", "flavor": "fresh", "ratings": [4]},
            {"id": "2", "name": "Steak", "price": 30.0, "diet": "meat", "flavor": "rich", "ratings": [5]},
            {"id": "3", "name": "Pasta", "price": 10.0, "diet": "vegetarian", "flavor": "savory", "ratings": [4]}
        ]
        
        prefs = {"vegetarian": 0.6}
        recommendations = recommend_meals(meals, prefs=prefs, budget=12.0, top_k=2, strategy="best")
        
        # Should get meals within budget
        for meal in recommendations:
            self.assertLessEqual(meal["price"], 12.0)


class TestPreferenceLearning(unittest.TestCase):
    """Test preference learning from history."""

    def test_learn_from_repeated_choices(self):
        """Test that repeated choices increase preference weights."""
        meals = [
            {"id": "1", "flavor": "spicy", "diet": "vegan"},
            {"id": "2", "flavor": "mild", "diet": "vegetarian"}
        ]
        
        history = ["1", "1", "1", "2"]  # Chose meal 1 three times
        weights = learn_preferences_from_history(meals, history)
        
        # Spicy and vegan should have higher weights
        self.assertGreater(weights.get("spicy", 0), weights.get("mild", 0))


class TestCompleteFilteringPipeline(unittest.TestCase):
    """Test complete filtering pipeline."""

    def test_diet_then_price_then_recommend(self):
        """Test filtering by diet, then price, then recommending."""
        menu = Menu()
        m1 = Meal("1", "Veg Salad", 7.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Veg Pasta", 9.0, 500, "vegetarian", "creamy")
        m3 = Meal("3", "Expensive Veg", 25.0, 600, "vegetarian", "fancy")
        m4 = Meal("4", "Burger", 10.0, 600, "meat", "savory")
        
        m1.add_rating(5)
        m2.add_rating(4)
        m3.add_rating(5)
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        menu.add(m4)
        
        # Filter vegetarian
        veg = menu.filter_by_diet("vegetarian")
        self.assertEqual(len(veg), 3)
        
        # Filter by price
        affordable = menu.filter_by_price(10.0)
        self.assertEqual(len(affordable), 3)  # All except expensive veg
        
        # Recommend
        meal_dicts = [m.to_dict() for m in menu.meals]
        prefs = {"vegetarian": 0.8}
        recommended = recommend_meals(meal_dicts, prefs=prefs, budget=10.0, top_k=2, strategy="best")
        
        self.assertLessEqual(len(recommended), 2)


if __name__ == "__main__":
    unittest.main()
