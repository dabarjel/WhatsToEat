import unittest
from meal_finder_library import (
    filter_by_diet,
    filter_by_price,
    add_rating,
    get_average_rating,
    compute_relevance_score
)


class TestMealIntegration(unittest.TestCase):

    def setUp(self):
        self.meals = [
            {"id": "1", "name": "Burger", "diet": "omnivore", "price": 12, "flavor": "savory"},
            {"id": "2", "name": "Salad", "diet": "vegetarian", "price": 9, "flavor": "fresh"},
            {"id": "3", "name": "Tofu Bowl", "diet": "vegan", "price": 10, "flavor": "savory"}
        ]
        self.ratings_db = {}

    # 1. Diet filter + price filter together
    def test_filter_by_diet_then_price(self):
        filtered = filter_by_diet(self.meals, "vegan")
        filtered = filter_by_price(filtered, 12)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "Tofu Bowl")

    # 2. Add rating then compute average rating
    def test_add_rating_then_average(self):
        add_rating(self.ratings_db, "1", 4)
        add_rating(self.ratings_db, "1", 5)
        avg = get_average_rating(self.ratings_db, "1")
        self.assertEqual(avg, 4.5)

    # 3. Multiple ratings across meals
    def test_multiple_meal_ratings(self):
        add_rating(self.ratings_db, "2", 3)
        add_rating(self.ratings_db, "2", 5)
        avg = get_average_rating(self.ratings_db, "2")
        self.assertEqual(avg, 4)

    # 4. Relevance scoring integrates preferences
    def test_compute_relevance_score(self):
        preferences = {"preferred_flavor": "savory"}
        scored = compute_relevance_score(self.meals, preferences)
        self.assertGreaterEqual(scored[0]["score"], scored[1]["score"])

    # 5. Integration of filtering + scoring
    def test_filter_and_score_workflow(self):
        filtered = filter_by_diet(self.meals, "vegetarian")
        preferences = {"preferred_flavor": "fresh"}
        scored = compute_relevance_score(filtered, preferences)
        self.assertEqual(scored[0]["name"], "Salad")


if __name__ == "__main__":
    unittest.main()
