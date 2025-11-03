MEAL CLASS

init(meal_id, name, price, calories, diet, flavor) – Creates a new Meal object with validated attributes for id, name, price, calories, diet, and flavor.
add_rating(rating) – Adds a user rating between 1 and 5 to the meal.
average_rating – Returns the average of all user ratings or 0 if no ratings exist.
format_meal() – Converts the meal into a readable string including id, name, price, and calories.
price (property) – Gets or sets the meal’s price with validation to ensure it is non-negative.
diet (property) – Returns the diet type (e.g., vegetarian, vegan, meat).
str() – Returns a short formatted meal description.
repr() – Returns a detailed string showing the meal’s internal data.

MENU CLASS

init(meals=None) – Creates a new Menu object containing a list of Meal objects.
from_csv(csv_text) – Converts a CSV string of meal data into structured Meal objects and returns a new Menu.
filter_by_diet(restriction) – Returns all meals that match a diet restriction (case-insensitive).
filter_by_price(max_price) – Returns all meals whose prices are less than or equal to max_price.
average_price() – Calculates the average price of all meals in the menu.
count_vegetarian() – Counts how many meals in the menu are vegetarian.
len() – Returns the total number of Meal objects in the menu.
iter() – Allows looping through all Meal objects.
str() – Returns a simple description such as “Menu with N meals.”
repr() – Returns a detailed developer-friendly string.

USER PREFERENCES CLASS

init(history_ids=None, budget=None) – Creates a UserPreferences object with optional meal history and spending budget.
add_meal_to_history(meal_id) – Adds a meal ID to the user’s selection history.
update_preferences(meals) – Learns preference weights for flavors and diets based on the user’s meal history.
check_budget(price) – Returns True if a meal’s price is within the user’s budget, otherwise False.
str() – Returns a readable summary of the user’s preferences and budget.
repr() – Returns a detailed internal string for debugging.

RECOMMENDATIONS CLASS

init(meals) – Creates a Recommendations system from an iterable of meal dictionaries.
add_to_history(meal_id) – Records a meal ID and updates the system’s learned flavor and diet preferences.
recommend_meals(top_k=3, budget=None, strategy="best", rng=None) – Suggests the top k meals that best match learned preferences, using “best,” “random,” or “hybrid” strategy.
suggest_by_flavor(flavor, budget=None) – Returns one random meal matching a given flavor keyword and optional budget limit.
_learn_preferences_from_history() – Internal helper that builds preference weights from the user’s meal history.
_compute_relevance_score(meal, prefs, budget=None) – Internal helper that calculates how relevant a meal is based on flavor/diet matches, ratings, and budget.
str() – Returns a short summary including total meals and number of history items.
repr() – Returns a detailed developer-friendly representation of the Recommendations object.
