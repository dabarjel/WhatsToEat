# WhatsToEat – Function Reference

This document is a reference for all functions we wrote in the WhatsToEat Meal Finder Library and includes a short description for what the function does. 

## SIMPLE FUNCTIONS
- **normalize_text(text)** – Removes extra spaces and capitalizes words.
- **within_budget(price, budget)** – Checks if a meal’s price falls within a given range.
- **is_valid_diet_type(diet)** – Verifies if a diet type is valid (vegan, vegetarian, etc.).
- **format_meal(meal)** – Converts a meal dictionary into a readable string. 
- **average_price(meals)** – Finds the average price from a list of meals. 

## MEDIUM FUNCTIONS
- **parse_menu_csv(csv_string)** – Converts a CSV string of meals into structured dictionaries.
- **filter_by_diet(meals, diet)** – Returns meals matching a given diet.
- **suggest_by_flavor(meals, flavor, budget=None)** – Returns meals matching a flavor preference.
- **filter_by_price(meals, max_price)** – Returns meals at or below a price limit.
- **add_rating(meal_id, rating)** – Stores or updates a user rating for a meal.
- **get_average_rating(meal)** - Finds the average of the meal.  
- **sort_meals_by_rating(meals)** – Sorts meals by their average user ratings.   

## COMPLEX FUNCTIONS
- **calculate_meal_score(meal)** – Computes a score using rating, calories, and price.
- **learn_preferences_from_history(meals, history_ids)** – Infers preferred diets and flavors from user rating patterns.
- **recommend_meals(meals, diet, flavor, top_k)** – Suggests meals that best match the user’s preferences. 
- **generate_analytics(meals,top_n=3)** – Creates a readable summary report of menu stats.  
