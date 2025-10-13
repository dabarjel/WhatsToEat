# WhatsToEat
### Team Members:
- Daniel Abarjel
- Ehsan Semati
- Brent Sare

## Project Overview
Python-based food recommendation and filtering system for students to pick meals based on budget, diet, and taste.

## How to Run
1. Clone or download repo
2. Run the demo: python examples/demo_script.py

## Domain Focus and Problem Statement
The domain focus of this project is in Library Management. It can be difficult finding what to eat sometimes. Users may have budget, dietary, food preference, or other concerns. The goal of this project is to help mitigate these issues and help users find meals that satisfy their concerns. This project will provide an organized library management system that helps users find their desired food options. 

# WhatsToEat – Function Reference and Key Functions

This document is a reference for all functions in the WhatsToEat Meal Finder Library and includes descriptions and examples.

## SIMPLE FUNCTIONS

### normalize_text(text)
Normalizes a string by stripping whitespace, converting to lowercase, and collapsing multiple spaces.

#### Example:
normalize_text("  Chicken   Salad  ")
# Output: "chicken salad"

### within_budget(price, budget)
Checks if a meal's price is within a given budget.

#### Example:
within_budget(8.50, 10)
# Output: True
within_budget(12, 10)
# Output: False

### format_meal(meal)
Returns a human-readable string describing a meal.

#### Example:
meal = {"id": 1, "name": "Chicken", "price": 8.50, "calories": 250}
format_meal(meal)
# Output: "Chicken (id:1) — $8.50, 250 kcal"

### average_price(meals)
Calculates the average price from a list of meals.

#### Example:
meals = [
    {"id": 1, "name": "Chicken", "price": 8.50},
    {"id": 2, "name": "Burger", "price": 10.00},
    {"id": 3, "name": "Salad", "price": 8.99}
]
average_price(meals)
# Output: 9.16

### count_vegetarian(meals)
Counts the number of meals that are vegetarian.

#### Example:
meals = [
    {"id": 1, "name": "Chicken", "diet": "regular"},
    {"id": 2, "name": "Salad", "diet": "vegetarian"}
]
count_vegetarian(meals)
# Output: 1

## MEDIUM FUNCTIONS

### parse_menu_csv(csv_text)
Parses a CSV string into a list of meal dictionaries. Requires columns: id,name,price,calories,diet,flavor.

#### Example:
csv_text = "id,name,price,calories,diet,flavor\n1,Chicken,8.50,250,regular,mild"
parse_menu_csv(csv_text)
# Output: [{'id': '1', 'name': 'Chicken', 'price': 8.5, 'calories': 250, 'diet': 'regular', 'flavor': 'mild', 'ratings': []}]

### filter_by_diet(meals, restriction)
Returns meals that match a dietary restriction (case-insensitive substring).

#### Example:
meals = [
    {"id": 1,"name": "Chicken", "price": 8.50, "diet": "regular", "flavor": "mild", "type": "entree"},
    {"id": 2, "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"}
]
filter_by_diet(meals, "Gluten-Free")
# Output: [{'id': 2, 'name': 'Burger', 'price': 10.00, 'diet': 'Gluten-Free', 'flavor': 'spicy', 'type': 'entree'}]

### filter_by_price(meals, max_price)
Returns meals at or below a given price.

#### Example:
meals = [
    {"id": 1,"name": "Chicken", "price": 8.50},
    {"id": 2, "name": "Burger", "price": 10.00}
]
filter_by_price(meals, 9)
# Output: [{'id': 1, 'name': 'Chicken', 'price': 8.50}]

### add_rating(meal, rating)
Adds a rating (1–5) to the meal’s "ratings" list in-place.

#### Example:
meal = {"id": 1, "name": "Chicken", "price": 8.50, "diet": "regular", "flavor": "mild", "type": "entree"}
add_rating(meal, 4)
add_rating(meal, 2)
meal
# Output: {'id': 1, 'name': 'Chicken', 'price': 8.50, 'diet': 'regular', 'flavor': 'mild', 'type': 'entree', 'ratings': [4,2]}

### get_average_rating(meal)
Returns the average rating for a meal (0 if no ratings).

#### Example:
meal = {"ratings": [4, 2, 5]}
get_average_rating(meal)
# Output: 3.67

### suggest_by_flavor(meals, flavor, budget=None)
Returns a random meal that matches the flavor (and optionally fits the budget).

#### Example:
meals = [
    {"id": 1, "name": "Spicy Chicken", "price": 8.5, "flavor": "spicy"},
    {"id": 2, "name": "Mild Salad", "price": 7.0, "flavor": "mild"}
]
suggest_by_flavor(meals, "spicy")
# Output: {'id': 1, 'name': 'Spicy Chicken', 'price': 8.5, 'flavor': 'spicy'}

## COMPLEX FUNCTIONS

### learn_preferences_from_history(meals, history_ids)
Learns user preference weights for flavor and diet tokens from meal history.

#### Example:
meals = [
    {"id": "1", "flavor": "spicy", "diet": "regular"},
    {"id": "2", "flavor": "mild", "diet": "vegetarian"}
]
history_ids = ["1", "2", "1"]
learn_preferences_from_history(meals, history_ids)
# Output: {'spicy': 0.4, 'regular': 0.4, 'mild': 0.2, 'vegetarian': 0.2}

### compute_relevance_score(meal, prefs, budget=None)
Computes a relevance score based on preference weights, average rating, and optional budget.

#### Example:
meal = {"flavor": "spicy", "diet": "regular", "ratings": [5]}
prefs = {'spicy': 0.5, 'regular': 0.5}
compute_relevance_score(meal, prefs, budget=10)
# Output: 6.0 (example, score may vary slightly)

### recommend_meals(meals, prefs=None, budget=None, top_k=3, strategy="best")
Recommends meals using 'best', 'random', or 'hybrid' strategy.

#### Example:
meals = [
    {"id": 1, "name": "Chicken", "price": 8.5, "flavor": "spicy", "ratings": [5]},
    {"id": 2, "name": "Salad", "price": 7.0, "flavor": "mild", "ratings": [3]}
]
recommend_meals(meals, top_k=1, strategy="best")
# Output: [{'id': 1, 'name': 'Chicken', 'price': 8.5, 'flavor': 'spicy', 'ratings': [5]}]

### generate_analytics(meals, top_n=3)
Computes analytics including top-rated meals, average price, min/max price, flavor counts, and total meals.

#### Example:
meals = [
    {"id": 1, "name": "Chicken", "price": 8.5, "flavor": "spicy", "ratings": [5]},
    {"id": 2, "name": "Salad", "price": 7.0, "flavor": "mild", "ratings": [3]}
]
generate_analytics(meals)
# Output:
# {
#   'top_rated': [{'id': 1, 'name': 'Chicken', 'avg_rating': 5.0}],
#   'avg_price': 7.75,
#   'min_price': 7.0,
#   'max_price': 8.5,
#   'flavor_counts': {'spicy': 1, 'mild': 1},
#   'total_meals': 2
# }
}
