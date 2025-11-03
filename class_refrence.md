MEAL CLASS

init(meal_id, name, price, calories, diet, flavor) – Creates a new Meal object, validates input types, and stores data in a dictionary for integration with the function library.
add_rating(rating) – Adds a rating (1–5) to the meal using the add_rating() function from the library.
average_rating – Returns the average user rating for the meal using the get_average_rating() function.
format_meal() – Produces a one-line formatted description using the format_meal() function.
to_dict() – Returns a dictionary copy of the meal’s data for use in library functions.
price (property) – Gets or sets the meal’s price with validation that it is non-negative.
calories (property) – Returns the calorie count for the meal.
diet (property) – Returns the diet type (e.g., vegetarian, vegan, meat).
flavor (property) – Returns the meal’s flavor description.
str() – Returns a readable formatted meal string.
repr() – Returns a detailed developer-friendly string containing meal data.

MENU CLASS

init(meals=None) – Initializes a Menu containing Meal objects with validation that each item is a Meal instance.
add(meal) – Adds a single Meal object to the menu, preventing duplicates by ID.
add_many(meals) – Adds multiple Meal objects at once, validating types and duplicates.
remove(meal_id) – Removes and returns a Meal by its ID, or None if not found.
get(meal_id) – Retrieves a Meal object by ID from the menu.
from_csv(csv_text) – Parses a CSV string of meals into a Menu and returns any row-level parsing errors.
filter_by_diet(restriction) – Returns a list of meals matching a dietary restriction (case-insensitive) using the filter_by_diet() function.
filter_by_price(max_price) – Returns meals priced at or below a given maximum using the filter_by_price() function.
average_price() – Computes and returns the average price of all meals in the menu using the average_price() function.
count_vegetarian() – Counts how many meals in the menu are vegetarian using the count_vegetarian() function.
recommend(prefs=None, budget=None, top_k=5, strategy="best") – Generates recommended meals using the recommend_meals() function from the library.
analytics() – Returns a summary dictionary of meal statistics and insights using the generate_analytics() function.
len() – Returns the number of Meal objects in the menu.
iter() – Enables iteration through all Meal objects in the menu.
str() – Returns a simple summary such as “Menu with N meals.”
repr() – Returns a concise developer-oriented description.

USER PREFERENCES CLASS

init(history_ids=None, budget=None) – Creates a UserPreferences object with optional meal history and budget validation.
add_meal_to_history(meal_id) – Adds a meal ID to the user’s history, ensuring it is valid and non-empty.
update_preferences(meals) – Learns token weights (flavor and diet preferences) from meal history using learn_preferences_from_history().
check_budget(price) – Checks whether a given price is within the user’s budget using the within_budget() function.
reset_history() – Clears the stored list of meal IDs from the user’s history.
reset_token_weights() – Clears all learned preference weights.
history_ids (property) – Returns a copy of the user’s saved meal history.
budget (property) – Gets or sets the user’s budget, ensuring it is non-negative or None.
token_weights (property) – Returns a dictionary of the learned flavor/diet token weights.
str() – Returns a readable summary of the user’s history and budget.
repr() – Returns a detailed representation for debugging.

RECOMMENDATIONS CLASS

init(meals) – Initializes the Recommendations system using a list of meal dictionaries.
add_to_history(meal_id) – Records a meal ID in the user’s history and triggers preference updates.
update_preferences() – Recomputes flavor and diet preferences using learn_preferences_from_history().
check_budget(price, budget=None) – Checks if a meal’s price is within a given budget using the within_budget() function.
recommend_meals(top_k=3, budget=None, strategy="best", rng=None) – Generates meal recommendations using the Project 1 recommend_meals() function and supports different strategies.
suggest_by_flavor(flavor, budget=None) – Suggests one random meal that matches a given flavor and optional budget using the suggest_by_flavor() function.
get_average_rating(meal_id) – Returns the average rating for a specific meal using get_average_rating().
reset_history() – Clears the user’s saved history and resets preferences.
reset_preferences() – Clears all learned preference weights.
str() – Returns a readable summary of total meals and history count.
repr() – Returns a developer-friendly string showing the Recommendations object details.
