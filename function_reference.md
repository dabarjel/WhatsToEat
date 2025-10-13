# WhatsToEat – Function Reference

This document is a reference for all functions we wrote in the WhatsToEat Meal Finder Library and includes a short description for what the function does. 

## SIMPLE FUNCTIONS
- **normalize_text(text)** – Normalizes text by stripping whitespace, lowercasing, and collapsing multiple spaces.
- **within_budget(price, budget)** – Checks if a meal’s price is less than or equal to a given budget.
- **format_meal(meal)** – Converts a meal dictionary into a readable string including id, name, price, and calories.
- **average_price(meals)** – Finds the average price from a list of meals.
- **count_vegetarian(meals)** – Counts how many meals are vegetarian based on the 'diet' field.

## MEDIUM FUNCTIONS
- **parse_menu_csv(csv_text)** – Converts a CSV string of meals into structured dictionaries.
- **filter_by_diet(meals, restriction)** – Returns meals matching a given diet (case-insensitive substring match).
- **filter_by_price(meals, max_price)** – Returns meals at or below a price limit.
- **add_rating(meal, rating)** – Adds a user rating (1–5) to a meal in-place.
- **get_average_rating(meal)** – Computes the average rating for a meal (0 if no ratings exist).
- **suggest_by_flavor(meals, flavor, budget=None)** – Returns a random meal matching a flavor preference, optionally filtered by budget.

## COMPLEX FUNCTIONS
- **compute_relevance_score(meal, prefs, budget=None)** – Computes a score using flavor/diet token matches, ratings, and budget proximity.
- **learn_preferences_from_history(meals, history_ids)** – Infers preferred diets and flavors from user history.
- **recommend_meals(meals, prefs=None, budget=None, top_k=3, strategy="best")** – Suggests meals that best match the user’s preferences using scoring or random/hybrid strategies.
- **generate_analytics(meals, top_n=3)** – Creates a summary report of menu stats including top-rated meals, price stats, and flavor counts.
