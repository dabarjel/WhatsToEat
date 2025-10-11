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
- add_rating(meal_id, rating): This function takes a meal's user rating then stores or updates it.
Example:
jim_meal = {"id": 1, "name": "Chicken", "price": 8.50, "diet": "regular","flavor": "mild", "type": "entree"}
add_rating(jim_meal, 4) 
add_rating(jim_meal, 2)
Output:
{'name': 'Chicken', 'price': 10.99, 'diet': 'vegetarian', "regular","flavor": "mild", "type": "entree", "ratings": [4,2]}

-filter_by_diet(meals, diet) – This function returns meals that match a given diet.
Example:
meals_list = [ {"id": 1,"name": "Chicken", "price": 8.50, "diet": "regular","flavor": "mild", "type": "entree"}
    {"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"},
    {"id": "3", "name": "Salad", "price": 8.99, "diet": "Vegetarian", "flavor": "mild", "type":},
    {"id": "4", "name": "Chili French Fries", "price": 4.00, "diet": "regular", "flavor": "spicy"}
  ]
filt_gluten = filter_by_diet(meals, "Gluten Free")
print(filt_gluten)

Output:
[{"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"}]

-average_price(meals) – This function calculates the average price from a list of meals.
Example:
john_meals = [ {"id": 1,"name": "Chicken", "price": 8.50, "diet": "regular","flavor": "mild", "type": "entree"},
    {"id": "2", "name": "Burger", "price": 10.00, "diet": "Gluten-Free", "flavor": "spicy", "type": "entree"},
    {"id": "3", "name": "Salad", "price": 8.99, "diet": "Vegetarian", "flavor": "mild", "type":"entree"},
    {"id": "4", "name": "Chili French Fries", "price": 4.00, "diet": "regular", "flavor": "spicy","type":"side"}
  ]
john_avg = average_price(john_meals)
print(john_avg)
Output:
$7.87
