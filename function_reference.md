# WhatsToEat – Function Reference

This document is a reference for all functions we wrote in the WhatsToEat Meal Finder Library and includes a short description for what the function does. 

## SIMPLE FUNCTIONS
- **clean_meal_name(name)** – Removes extra spaces and capitalizes words.
- **validate_price_range(price, min_price, max_price)** – Checks if a meal’s price falls within a given range.
- **is_valid_diet_type(diet)** – Verifies if a diet type is valid (vegan, vegetarian, etc.).
- **format_meal_entry(meal)** – Converts a meal dictionary into a readable string. 
- **calculate_average_price(meals)** – Finds the average price from a list of meals. 

## MEDIUM FUNCTIONS
- **parse_menu_csv(csv_string)** – Converts a CSV string of meals into structured dictionaries.
- **filter_meals_by_diet(meals, diet)** – Returns meals matching a given diet.
- **filter_meals_by_flavor(meals, flavor)** – Returns meals matching a flavor preference.
- **filter_meals_by_budget(meals, max_price)** – Returns meals at or below a price limit.
- **rate_meal(meal_id, rating)** – Stores or updates a user rating for a meal.  
- **sort_meals_by_rating(meals)** – Sorts meals by their average user ratings.   

## COMPLEX FUNCTIONS
- **calculate_meal_score(meal)** – Computes a score using rating, calories, and price.
- **learn_user_preferences(ratings)** – Infers preferred diets and flavors from user rating patterns.
- **recommend_meals(meals, diet, flavor, top_k)** – Suggests meals that best match the user’s preferences. 
- **generate_summary_report(meals)** – Creates a readable summary report of menu stats.  
