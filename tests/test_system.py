"""System tests - complete end-to-end workflows."""

import unittest
from information_retreival_MealClass import Meal
from information_retreival_MenuClass import Menu
from information_retreival_UserPreferences import UserPreferences


class TestCompleteUserWorkflow(unittest.TestCase):
    """Test complete user interaction workflows."""

    def test_new_user_finds_meal(self):
        """Test a new user finding and selecting a meal."""
        # Step 1: Create menu
        menu = Menu()
        m1 = Meal("1", "Spicy Tofu Bowl", 9.99, 450, "vegan", "spicy")
        m2 = Meal("2", "Chicken Salad", 11.99, 500, "meat", "fresh")
        m3 = Meal("3", "Veggie Burger", 8.99, 400, "vegetarian", "savory")
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        
        # Step 2: User sets budget
        user_prefs = UserPreferences(budget=12.0)
        
        # Step 3: User filters by diet
        veg_options = menu.filter_by_diet("vegan")
        self.assertGreater(len(veg_options), 0)
        
        # Step 4: User checks if affordable
        selected_meal = veg_options[0]
        is_affordable = user_prefs.check_budget(selected_meal.price)
        self.assertTrue(is_affordable)
        
        # Step 5: User adds to history
        user_prefs.add_meal_to_history(selected_meal.id)
        self.assertEqual(len(user_prefs.history_ids), 1)

    def test_returning_user_gets_recommendations(self):
        """Test returning user getting personalized recommendations."""
        # Step 1: Setup menu
        menu = Menu()
        m1 = Meal("1", "Spicy Curry", 10.0, 500, "vegan", "spicy")
        m2 = Meal("2", "Mild Pasta", 9.0, 450, "vegetarian", "mild")
        m3 = Meal("3", "Spicy Tofu", 8.0, 400, "vegan", "spicy")
        
        m1.add_rating(5)
        m2.add_rating(3)
        m3.add_rating(4)
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        
        # Step 2: User has history (previously ordered spicy vegan meals)
        user_prefs = UserPreferences(history_ids=["1", "3"], budget=12.0)
        
        # Step 3: Learn preferences from history
        meal_dicts = [m.to_dict() for m in menu.meals]
        user_prefs.update_preferences(meal_dicts)
        
        # Step 4: Get recommendations
        recommended = menu.recommend(
            prefs=user_prefs.token_weights,
            budget=user_prefs.budget,
            top_k=2,
            strategy="best"
        )
        
        # Should recommend spicy vegan meals
        self.assertGreater(len(recommended), 0)
        self.assertLessEqual(recommended[0].price, user_prefs.budget)


class TestDataImportAndAnalytics(unittest.TestCase):
    """Test importing data and generating analytics."""

    def test_csv_import_and_analytics(self):
        """Test complete workflow from CSV import to analytics."""
        # Step 1: Import from CSV
        csv_data = """id,name,price,calories,diet,flavor
1,Salad,8.5,300,vegetarian,fresh
2,Burger,10.0,600,meat,savory
3,Pasta,9.5,500,vegetarian,creamy"""
        
        menu, errors = Menu.from_csv(csv_data)
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(menu), 3)
        
        # Step 2: Add ratings
        for meal in menu:
            meal.add_rating(4)
            meal.add_rating(5)
        
        # Step 3: Generate analytics
        analytics = menu.analytics()
        
        # Verify analytics
        self.assertEqual(analytics["total_meals"], 3)
        self.assertGreater(analytics["avg_price"], 0)
        self.assertIsNotNone(analytics["min_price"])
        self.assertIsNotNone(analytics["max_price"])


class TestBudgetConstrainedSearch(unittest.TestCase):
    """Test searching for meals with budget constraints."""

    def test_find_affordable_vegetarian_meals(self):
        """Test finding vegetarian meals within budget."""
        # Setup
        menu = Menu()
        m1 = Meal("1", "Cheap Salad", 6.0, 250, "vegetarian", "fresh")
        m2 = Meal("2", "Expensive Truffle Pasta", 35.0, 600, "vegetarian", "fancy")
        m3 = Meal("3", "Regular Veggie Bowl", 9.0, 400, "vegetarian", "savory")
        m4 = Meal("4", "Burger", 11.0, 550, "meat", "savory")
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        menu.add(m4)
        
        # User wants vegetarian under $10
        user_prefs = UserPreferences(budget=10.0)
        
        # Filter by diet
        veg_meals = menu.filter_by_diet("vegetarian")
        
        # Check which are affordable
        affordable_veg = [m for m in veg_meals if user_prefs.check_budget(m.price)]
        
        self.assertEqual(len(affordable_veg), 2)
        for meal in affordable_veg:
            self.assertLessEqual(meal.price, 10.0)


class TestRatingAndRecommendation(unittest.TestCase):
    """Test rating workflow affecting recommendations."""

    def test_highly_rated_meals_recommended_first(self):
        """Test that highly rated meals are recommended first."""
        # Create meals with different ratings
        menu = Menu()
        m1 = Meal("1", "Average Meal", 10.0, 500, "vegetarian", "mild")
        m2 = Meal("2", "Great Meal", 10.0, 500, "vegetarian", "mild")
        m3 = Meal("3", "Poor Meal", 10.0, 500, "vegetarian", "mild")
        
        # Add ratings
        m1.add_rating(3)
        m1.add_rating(3)
        
        m2.add_rating(5)
        m2.add_rating(5)
        
        m3.add_rating(2)
        m3.add_rating(2)
        
        menu.add(m1)
        menu.add(m2)
        menu.add(m3)
        
        # Get recommendations
        meal_dicts = [m.to_dict() for m in menu.meals]
        from meal_finder_library import recommend_meals
        
        recommendations = recommend_meals(
            meal_dicts,
            prefs={"vegetarian": 0.5, "mild": 0.5},
            top_k=3,
            strategy="best"
        )
        
        # Highest rated should be first
        self.assertEqual(recommendations[0]["name"], "Great Meal")


class TestEmptyAndEdgeCases(unittest.TestCase):
    """Test edge cases and empty states."""

    def test_empty_menu_operations(self):
        """Test operations on empty menu."""
        menu = Menu()
        
        self.assertEqual(len(menu), 0)
        self.assertEqual(menu.average_price(), 0.0)
        self.assertEqual(menu.count_vegetarian(), 0)
        
        filtered = menu.filter_by_diet("vegetarian")
        self.assertEqual(len(filtered), 0)

    def test_no_matching_meals(self):
        """Test when no meals match criteria."""
        menu = Menu()
        m1 = Meal("1", "Burger", 10.0, 500, "meat", "savory")
        menu.add(m1)
        
        # Search for vegetarian (none exist)
        veg_meals = menu.filter_by_diet("vegetarian")
        self.assertEqual(len(veg_meals), 0)


if __name__ == "__main__":
    unittest.main()
