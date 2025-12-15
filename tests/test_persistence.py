"""Persistence tests - testing save/load functionality (CRITICAL FOR PROJECT 4)."""

import unittest
import os
import json
from pathlib import Path
from information_retreival_MealClass import Meal
from information_retreival_MenuClass import Menu
from information_retreival_UserPreferences import UserPreferences


class TestMenuPersistence(unittest.TestCase):
    """Test Menu save and load functionality."""

    def setUp(self):
        """Set up test directory."""
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)
        self.menu_file = self.test_dir / "test_menu.json"

    def tearDown(self):
        """Clean up test files."""
        if self.menu_file.exists():
            self.menu_file.unlink()
        if self.test_dir.exists():
            self.test_dir.rmdir()

    def test_save_menu(self):
        """Test saving menu to file."""
        menu = Menu()
        m1 = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        m2 = Meal("2", "Burger", 10.0, 500, "meat", "savory")
        menu.add(m1)
        menu.add(m2)
        
        menu.save_to_file(str(self.menu_file))
        
        # Verify file exists
        self.assertTrue(self.menu_file.exists())

    def test_load_menu(self):
        """Test loading menu from file."""
        # Create and save menu
        menu = Menu()
        m1 = Meal("1", "Pasta", 12.5, 600, "vegetarian", "savory")
        m1.add_rating(5)
        menu.add(m1)
        menu.save_to_file(str(self.menu_file))
        
        # Load menu
        loaded_menu = Menu.load_from_file(str(self.menu_file))
        
        # Verify data
        self.assertEqual(len(loaded_menu), 1)
        meal = loaded_menu.get("1")
        self.assertEqual(meal.name, "Pasta")
        self.assertEqual(meal.price, 12.5)
        self.assertEqual(meal.average_rating, 5.0)

    def test_save_load_roundtrip(self):
        """Test that save then load preserves all data."""
        # Create menu with multiple meals and ratings
        menu = Menu()
        m1 = Meal("1", "Salad", 8.0, 300, "vegetarian", "fresh")
        m2 = Meal("2", "Steak", 25.0, 700, "meat", "rich")
        
        m1.add_rating(5)
        m1.add_rating(4)
        m2.add_rating(3)
        
        menu.add(m1)
        menu.add(m2)
        
        # Save
        menu.save_to_file(str(self.menu_file))
        
        # Load
        loaded = Menu.load_from_file(str(self.menu_file))
        
        # Verify everything matches
        self.assertEqual(len(loaded), 2)
        
        loaded_m1 = loaded.get("1")
        self.assertEqual(loaded_m1.name, "Salad")
        self.assertEqual(loaded_m1.average_rating, 4.5)
        
        loaded_m2 = loaded.get("2")
        self.assertEqual(loaded_m2.name, "Steak")
        self.assertEqual(loaded_m2.average_rating, 3.0)


class TestUserPreferencesPersistence(unittest.TestCase):
    """Test UserPreferences save and load functionality."""

    def setUp(self):
        """Set up test directory."""
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)
        self.prefs_file = self.test_dir / "test_prefs.json"

    def tearDown(self):
        """Clean up test files."""
        if self.prefs_file.exists():
            self.prefs_file.unlink()
        if self.test_dir.exists():
            self.test_dir.rmdir()

    def test_save_preferences(self):
        """Test saving user preferences to file."""
        prefs = UserPreferences(history_ids=["1", "2", "3"], budget=15.0)
        prefs._token_weights = {"spicy": 0.6, "vegan": 0.4}
        
        prefs.save_to_file(str(self.prefs_file))
        
        # Verify file exists
        self.assertTrue(self.prefs_file.exists())

    def test_load_preferences(self):
        """Test loading user preferences from file."""
        # Create and save
        prefs = UserPreferences(history_ids=["1", "2"], budget=12.0)
        prefs._token_weights = {"spicy": 0.5, "vegetarian": 0.5}
        prefs.save_to_file(str(self.prefs_file))
        
        # Load
        loaded = UserPreferences.load_from_file(str(self.prefs_file))
        
        # Verify
        self.assertEqual(loaded.history_ids, ["1", "2"])
        self.assertEqual(loaded.budget, 12.0)
        self.assertIn("spicy", loaded.token_weights)

    def test_preferences_roundtrip(self):
        """Test preferences save/load preserves all data."""
        prefs = UserPreferences(history_ids=["1", "3", "5"], budget=20.0)
        prefs._token_weights = {"mild": 0.3, "spicy": 0.7}
        
        prefs.save_to_file(str(self.prefs_file))
        loaded = UserPreferences.load_from_file(str(self.prefs_file))
        
        self.assertEqual(loaded.history_ids, ["1", "3", "5"])
        self.assertEqual(loaded.budget, 20.0)
        self.assertEqual(loaded.token_weights, {"mild": 0.3, "spicy": 0.7})


class TestPersistenceErrorHandling(unittest.TestCase):
    """Test error handling in persistence operations."""

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        with self.assertRaises(FileNotFoundError):
            Menu.load_from_file("nonexistent.json")

    def test_load_invalid_json(self):
        """Test loading invalid JSON raises error."""
        test_file = Path("test_data/invalid.json")
        test_file.parent.mkdir(exist_ok=True)
        
        # Write invalid JSON
        with open(test_file, 'w') as f:
            f.write("not valid json{")
        
        with self.assertRaises(ValueError):
            Menu.load_from_file(str(test_file))
        
        # Cleanup
        test_file.unlink()
        test_file.parent.rmdir()


class TestCSVImport(unittest.TestCase):
    """Test CSV import functionality."""

    def test_import_csv_basic(self):
        """Test basic CSV import."""
        csv_text = """id,name,price,calories,diet,flavor
1,Salad,8.5,300,vegetarian,fresh
2,Burger,10.0,600,meat,savory"""
        
        menu, errors = Menu.from_csv(csv_text)
        
        self.assertEqual(len(errors), 0)
        self.assertEqual(len(menu), 2)
        
        meal1 = menu.get("1")
        self.assertEqual(meal1.name, "Salad")
        self.assertEqual(meal1.price, 8.5)

    def test_import_csv_with_errors(self):
        """Test CSV import handles missing columns."""
        csv_text = """id,name,price
1,Salad,8.5"""
        
        menu, errors = Menu.from_csv(csv_text)
        
        # Should have errors due to missing columns
        self.assertGreater(len(errors), 0)


class TestAnalyticsExport(unittest.TestCase):
    """Test analytics export functionality."""

    def test_export_analytics_to_json(self):
        """Test exporting analytics to JSON file."""
        # Create menu
        menu = Menu()
        m1 = Meal("1", "Pasta", 12.0, 600, "vegetarian", "savory")
        m2 = Meal("2", "Salad", 8.0, 300, "vegetarian", "fresh")
        
        m1.add_rating(5)
        m2.add_rating(4)
        
        menu.add(m1)
        menu.add(m2)
        
        # Generate analytics
        analytics = menu.analytics()
        
        # Export to JSON
        test_dir = Path("test_data")
        test_dir.mkdir(exist_ok=True)
        analytics_file = test_dir / "analytics.json"
        
        with open(analytics_file, 'w') as f:
            json.dump(analytics, f, indent=2)
        
        # Verify file exists and is valid JSON
        self.assertTrue(analytics_file.exists())
        
        with open(analytics_file, 'r') as f:
            loaded_analytics = json.load(f)
        
        self.assertEqual(loaded_analytics["total_meals"], 2)
        self.assertGreater(loaded_analytics["avg_price"], 0)
        
        # Cleanup
        analytics_file.unlink()
        test_dir.rmdir()


class TestCompleteDataPersistenceWorkflow(unittest.TestCase):
    """Test complete data persistence workflow."""

    def setUp(self):
        """Set up test directory."""
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)

    def tearDown(self):
        """Clean up all test files."""
        for file in self.test_dir.glob("*"):
            file.unlink()
        self.test_dir.rmdir()

    def test_full_session_persistence(self):
        """Test saving and restoring a complete user session."""
        # Session 1: User creates preferences and orders
        menu = Menu()
        m1 = Meal("1", "Spicy Tofu", 9.0, 400, "vegan", "spicy")
        m2 = Meal("2", "Mild Pasta", 11.0, 500, "vegetarian", "mild")
        
        m1.add_rating(5)
        m2.add_rating(3)
        
        menu.add(m1)
        menu.add(m2)
        
        prefs = UserPreferences(history_ids=["1", "1"], budget=15.0)
        prefs.update_preferences([m.to_dict() for m in menu.meals])
        
        # Save everything
        menu_file = self.test_dir / "menu.json"
        prefs_file = self.test_dir / "prefs.json"
        
        menu.save_to_file(str(menu_file))
        prefs.save_to_file(str(prefs_file))
        
        # Session 2: User returns later, load everything
        loaded_menu = Menu.load_from_file(str(menu_file))
        loaded_prefs = UserPreferences.load_from_file(str(prefs_file))
        
        # Verify session restored correctly
        self.assertEqual(len(loaded_menu), 2)
        self.assertEqual(loaded_prefs.history_ids, ["1", "1"])
        self.assertIn("spicy", loaded_prefs.token_weights)
        
        # User continues using system
        loaded_prefs.add_meal_to_history("2")
        self.assertEqual(len(loaded_prefs.history_ids), 3)


if __name__ == "__main__":
    unittest.main()
