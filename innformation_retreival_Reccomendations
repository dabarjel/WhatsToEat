from typing import Any, Dict, Iterable, List, Optional
import random
import statistics

Meal = Dict[str, Any]


class Recommendations:
    """
    Simple meal recommendation system.
    
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
        """
        Initialize the Recommendations object.

        Args:
            meals: Iterable of meal dictionaries (must contain 'id', 'name', 'price').

        Raises:
            TypeError: if meals is not iterable
        """
        if meals is None or not hasattr(meals, "__iter__"):
            raise TypeError("meals must be an iterable of meal dictionaries")
        self._meals: List[Meal] = [m for m in meals if isinstance(m, dict)]
        self._history_ids: List[str] = []
        self._prefs: Dict[str, float] = {}

    @property
    def meals(self) -> List[Meal]:
        """List of all available meals (read-only)."""
        return self._meals.copy()

    @property
    def history_ids(self) -> List[str]:
        """User's meal history (read-only)."""
        return self._history_ids.copy()

    @property
    def prefs(self) -> Dict[str, float]:
        """Current learned preference weights (read-only)."""
        return self._prefs.copy()

    def add_to_history(self, meal_id: str) -> None:
        """
        Add a meal ID to user history and update preferences.

        Args:
            meal_id: ID of the meal to add

        Raises:
            TypeError: if meal_id is not a string
        """
        if not isinstance(meal_id, str):
            raise TypeError("meal_id must be a string")
        self._history_ids.append(meal_id)
        self._learn_preferences_from_history()

    def recommend_meals(
        self,
        top_k: int = 3,
        budget: Optional[float] = None,
        strategy: str = "best",
        rng: Optional[random.Random] = None
    ) -> List[Meal]:
        """
        Recommend meals based on learned preferences.

        Args:
            top_k: number of meals to return (default 3)
            budget: optional budget to filter/penalize
            strategy: 'best', 'random', or 'hybrid' (default 'best')
            rng: optional random.Random instance for deterministic results

        Returns:
            List of recommended meal dictionaries
        """
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be an int >= 1")
        if strategy not in {"best", "random", "hybrid"}:
            raise ValueError("strategy must be 'best', 'random', or 'hybrid'")

        rng = rng or random.Random()
        candidates = [m for m in self._meals if "id" in m and "name" in m and "price" in m]

        if not candidates:
            return []

        if strategy == "random":
            picks = []
            pool = list(candidates)
            while pool and len(picks) < top_k:
                pick = rng.choice(pool)
                picks.append(pick)
                pool.remove(pick)
            return picks

        # Compute relevance scores
        scored = [(self._compute_relevance_score(m, self._prefs, budget), m) for m in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:top_k]]

    def suggest_by_flavor(self, flavor: str, budget: Optional[float] = None) -> Optional[Meal]:
        """
        Suggest a single meal matching a flavor and optional budget.

        Args:
            flavor: flavor keyword to match (case-insensitive)
            budget: optional maximum price

        Returns:
            A single meal dictionary or None if no match
        """
        if not isinstance(flavor, str):
            raise TypeError("flavor must be a string")
        candidates = [
            m for m in self._meals
            if flavor.lower() in str(m.get("flavor", "")).lower()
            and (budget is None or (isinstance(m.get("price"), (int, float)) and m["price"] <= budget))
        ]
        return random.choice(candidates) if candidates else None

    # ----------------- Private helper methods -----------------
    def _learn_preferences_from_history(self) -> None:
        """Update preference weights from the current history."""
        token_counts: Dict[str, int] = {}
        total = 0
        meal_map = {str(m["id"]): m for m in self._meals if "id" in m}

        for hid in self._history_ids:
            meal = meal_map.get(str(hid))
            if not meal:
                continue
            flavor = str(meal.get("flavor", "")).lower()
            diet = str(meal.get("diet", "")).lower()
            tokens = []
            for part in (flavor.split(",") + diet.split(",")):
                for token in part.strip().split():
                    t = token.strip()
                    if t:
                        tokens.append(t)
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1
                total += 1
        self._prefs = {k: v / total for k, v in token_counts.items()} if total > 0 else {}

    def _compute_relevance_score(self, meal: Meal, prefs: Dict[str, float], budget: Optional[float] = None) -> float:
        """Compute a simple relevance score for a meal."""
        flavor = str(meal.get("flavor", "")).lower()
        diet = str(meal.get("diet", "")).lower()
        tokens = {t.strip() for part in (flavor.split(",") + diet.split(",")) for t in part.strip().split() if t}
        token_score = sum(float(prefs.get(t, 0.0)) for t in tokens)
        rating_avg = float(statistics.mean(meal.get("ratings", []) or [0]))
        budget_effect = 0.0
        if budget is not None and isinstance(meal.get("price"), (int, float)):
            price = float(meal["price"])
            if price <= budget:
                budget_effect += max(0.0, 1.0 - ((budget - price) / max(1.0, budget))) * 0.5
            else:
                budget_effect -= (price - budget) * 0.2
        return token_score * 2.0 + rating_avg + budget_effect

    # ----------------- String representations -----------------
    def __str__(self) -> str:
        return f"<Recommendations: {len(self._meals)} meals, {len(self._history_ids)} history items>"

    def __repr__(self) -> str:
        return f"Recommendations(meals={self._meals!r})"
