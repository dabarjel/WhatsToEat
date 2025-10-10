from src.meal_finder_library import *

meals = [
    {"name": "Veggie Burrito", "price": 8.5, "diet": "vegetarian", "flavor": "spicy", "type": "entree"},
    {"name": "Chicken Sandwich", "price": 10.0, "diet": "regular", "flavor": "savory", "type": "entree"},
    {"name": "Salad Bowl", "price": 7.0, "diet": "vegan", "flavor": "fresh", "type": "side"},
]

prefs = {"flavor": "spicy", "diet": "vegetarian", "type": "entree"}

print("=== Example Recommendations ===")
print(recommend_meals(meals, prefs, budget=12, top_k=2))
print("=== Analytics ===")
print(generate_analytics(meals))
