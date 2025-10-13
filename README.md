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

## Key Functions 

### add_rating(meal, rating): 
This function takes a meal's user rating then stores or updates it.
  
#### Example:
jim_meal = {"id": 1, "name": "Chicken", "price": 8.50, "diet": "regular", "flavor": "mild", "type": "entree"}
add_rating(jim_meal, 4) 
add_rating(jim_meal, 2)

#### Output:
{'id': 1, 'name': 'Chicken', 'price': 8.50, 'diet': 'regular', 'flavor': 'mild', 'type': 'entree', 'ratings': [4, 2]}


### filter_by_diet(meals, restriction):
This function returns meals that match a given diet.
  
#### Example:
meals_list = [
    {"id": 1, "name": "Chicken", "price": 8.50, "diet": "regular", "flavor": "mild", "type": "entree"},
    {"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"},
    {"id": "3", "name": "Salad", "price": 8.99, "diet": "Vegetarian", "flavor": "mild", "type": "entree"},
    {"id": "4", "name": "Chili French Fries", "price": 4.00, "diet": "regular", "flavor": "spicy", "type": "side"}
]
filt_gluten = filter_by_diet(meals_list, "Gluten-Free")

print(filt_gluten)

#### Output:
[{"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"}]


### average_price(meals):
This function calculates the average price from a list of meals.

#### Example:
john_meals = [
    {"id": 1, "name": "Chicken", "price": 8.50, "diet": "regular", "flavor": "mild", "type": "entree"},
    {"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"},
    {"id": "3", "name": "Salad", "price": 8.99, "diet": "Vegetarian", "flavor": "mild", "type": "entree"},
    {"id": "4", "name": "Chili French Fries", "price": 4.00, "diet": "regular", "flavor": "spicy", "type": "side"}
]

john_avg = average_price(john_meals)
print(john_avg)

#### Output:
7.87


### suggest_by_flavor(meals, flavor, budget=None):
This function returns a random meal that matches a flavor and optionally fits a budget.

#### Example:
meal_options = [
    {"id": 1, "name": "Spicy Tofu", "price": 9.50, "diet": "Vegetarian", "flavor": "spicy", "type": "entree"},
    {"id": 2, "name": "Mild Curry", "price": 12.00, "diet": "Vegan", "flavor": "mild", "type": "entree"},
    {"id": 3, "name": "Hot Wings", "price": 11.00, "diet": "Regular", "flavor": "spicy", "type": "entree"}
]
chosen = suggest_by_flavor(meal_options, "spicy", budget=10.00)

print(chosen)

#### Output (example):
{'id': 1, 'name': 'Spicy Tofu', 'price': 9.50, 'diet': 'Vegetarian', 'flavor': 'spicy', 'type': 'entree'}


### learn_preferences_from_history(meals, history_ids):
This function infers preferred diets and flavors from a user’s meal history.

#### Example:
meal_history = ["1", "3"]
prefs = learn_preferences_from_history(meal_options, meal_history)

print(prefs)

#### Output (example):
{'spicy': 0.66, 'vegetarian': 0.33, 'regular': 0.33}


### recommend_meals(meals, prefs=None, budget=None, top_k=3, strategy='best'):
This function recommends meals based on preferences, budget, and strategy.

#### Example:
recommendations = recommend_meals(meal_options, prefs=prefs, budget=12, top_k=2, strategy='best')

print(recommendations)

#### Output (example):
[
    {'id': 1, 'name': 'Spicy Tofu', 'price': 9.50, 'diet': 'Vegetarian', 'flavor': 'spicy', 'type': 'entree', 'ratings': []},
    {'id': 3, 'name': 'Hot Wings', 'price': 11.00, 'diet': 'Regular', 'flavor': 'spicy', 'type': 'entree', 'ratings': []}
]


### generate_analytics(meals, top_n=3):
This function creates a summary report of menu stats.

#### Example:
analytics = generate_analytics(meal_options, top_n=2)

print(analytics)

#### Output (example):
{
    'top_rated': [],
    'avg_price': 10.83,
    'min_price': 9.50,
    'max_price': 12.00,
    'flavor_counts': {'spicy': 2, 'mild': 1},
    'total_meals': 3
}
