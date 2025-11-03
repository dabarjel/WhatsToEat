from typing import Any, Dict, Iterable, List, Optional
import random

# Import Project 1 functions
from meal_finder_library import (
    learn_preferences_from_history,
    within_budget,
    get_average_rating,
    suggest_by_flavor,
    recommend_meals
)

Meal = Dict[str, Any]

class Recommendations:
    """
    Meal recommendation system using Project 1 functions.

    Tracks user history and makes suggestions based on learned preferences.

    Example:
        meals = [
            {"id": "1", "name": "Spicy Tofu", "price": 10, "flavor": "spicy", "diet": "vegetarian", "ratings": [5, 4]},
            {"id": "2", "name": "Chicken Curry", "price": 12, "flavor": "spicy", "diet": "meat", "ratings": [4, 4]},
        ]
        rec = Recommendations(meals)
        rec.add_to_history("1")
        top = rec.recommend_meals(top_k=1)
        spicy_meal = rec.suggest_by_flavor("spicy")
    """

    def __init__(self, meals: Iterable[Meal]):
        #Initialize Recommendations with a list of meals.
        if meals is None or not hasattr(meals, "__iter__"):
            raise TypeError("meals must be an iterable of meal dictionaries")
        self._meals: List[Meal] = [m for m in meals if isinstance(m, dict)]
        self._history_ids: List[str] = []
        self._prefs: Dict[str, float] = {}

    @property
    def meals(self) -> List[Meal]:
        return self._meals.copy()

    @property
    def history_ids(self) -> List[str]:
        return self._history_ids.copy()

    @property
    def prefs(self) -> Dict[str, float]:
        return self._prefs.copy()

    def add_to_history(self, meal_id: str) -> None:
        #Add a meal ID to history and update preferences.
        if not isinstance(meal_id, str):
            raise TypeError("meal_id must be a string")
        self._history_ids.append(meal_id)
        self.update_preferences()

    def update_preferences(self) -> None:
        #Update preference weights from current history using Project 1.
        self._prefs = learn_preferences_from_history(self._meals, self._history_ids)

    def check_budget(self, price: float, budget: Optional[float] = None) -> bool:
        # Check if a meal price is within a given budget.
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price < 0:
            raise ValueError("price must be non-negative")
        if budget is None:
            return True
        return within_budget(price, budget)

    def recommend_meals(
        self,
        top_k: int = 3,
        budget: Optional[float] = None,
        strategy: str = "best",
        rng: Optional[random.Random] = None
    ) -> List[Meal]:
        # Recommend meals using Project 1 recommend_meals function.
        return recommend_meals(
            meals=self._meals,
            prefs=self._prefs,
            budget=budget,
            top_k=top_k,
            strategy=strategy,
            rng=rng
        )

    def suggest_by_flavor(self, flavor: str, budget: Optional[float] = None) -> Optional[Meal]:
        #Suggest a single meal by flavor using Project 1 function.
        return suggest_by_flavor(self._meals, flavor, budget)

    def get_average_rating(self, meal_id: str) -> float:
        #Get the average rating of a meal using Project 1 get_average_rating.
        meal = next((m for m in self._meals if str(m.get("id")) == str(meal_id)), None)
        if not meal:
            return 0.0
        return get_average_rating(meal)

    def reset_history(self) -> None:
        #Clear user meal history.
        self._history_ids.clear()
        self.update_preferences()

    def reset_preferences(self) -> None:
        #Clear learned preferences.
        self._prefs.clear()

    def __str__(self) -> str:
        return f"<Recommendations: {len(self._meals)} meals, {len(self._history_ids)} history items>"

    def __repr__(self) -> str:
        return f"Recommendations(meals={self._meals!r})"
