import unittest
from meal_finder_library import (
    filter_by_diet,
    filter_by_price,
    add_rating,
    get_average_rating,
    compute_relevance_score
)


class TestSystemWorkflows(unittest.TestCase):

    def setUp(self):
        self.meals = [
            {"id": "1", "name": "Burger", "diet": "omnivore", "price": 12, "flavor": "savory"},
            {"id": "2", "name": "Salad", "diet": "vegetarian", "price": 9, "flavor": "fresh"},
            {"id": "3", "name": "Tofu Bowl", "diet": "vegan", "price": 10, "flavor": "savory"}
        ]
        self.ratings_db = {}

    # 1. Full recommendation workflow
    def test_full_recommendation_workflow(self):
        filtered = filter_by_diet(self.meals, "vegan")
        filtered = filter_by_price(filtered, 15)

        preferences = {"preferred_flavor": "savory"}
        scored = compute_relevance_score(filtered, preferences)

        self.assertEqual(len(scored), 1)
        self.assertEqual(scored[0]["name"], "Tofu Bowl")

    # 2. Ratings affect final outcome
    def test_ratings_influence_results(self):
        add_rating(self.ratings_db, "1", 5)
        add_rating(self.ratings_db, "1", 4)

        avg = get_average_rating(self.ratings_db, "1")
        self.assertEqual(avg, 4.5)

    # 3. No matching meals returns empty result
    def test_no_matching_meals(self):
        filtered = filter_by_diet(self.meals, "keto")
        self.assertEqual(filtered, [])

    # 4. Multiple filters + scoring
    def test_multiple_constraints_workflow(self):
        filtered = filter_by_diet(self.meals, "vegetarian")
        filtered = filter_by_price(filtered, 10)

        preferences = {"preferred_flavor": "fresh"}
        scored = compute_relevance_score(filtered, preferences)

        self.assertEqual(scored[0]["name"], "Salad")


if __name__ == "__main__":
    unittest.main()
