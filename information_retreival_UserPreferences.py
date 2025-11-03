from __future__ import annotations
from typing import Dict, List, Optional, Iterable

class UserPreferences:
    """Represents a user's meal preferences (history + budget + learned weights).

    Tracks the user's meal history, budget, and learned flavor/diet token weights.

    Example:
        >>> prefs = UserPreferences(history_ids=["1", "2"], budget=15.0)
        >>> prefs.add_meal_to_history("3")
        >>> prefs.check_budget(10)
        True
        >>> prefs.token_weights  # after update_preferences(menu)
        {'spicy': 0.5, 'vegetarian': 0.5, ...}
    """

    def __init__(self, history_ids: Optional[List[str]] = None, budget: Optional[float] = None) -> None:
        """Initialize UserPreferences with optional meal history and budget.

        Args:
            history_ids (list[str] | None): Prior selected meal ids.
            budget (float | None): Optional non-negative spending cap.

        Raises:
            TypeError: If types are invalid.
            ValueError: If budget is negative or any id is blank.
        """
        # Validate types
        if history_ids is not None and not isinstance(history_ids, list):
            raise TypeError("history_ids must be a list[str] or None")
        if budget is not None and not isinstance(budget, (int, float)):
            raise TypeError("budget must be a number or None")
        if budget is not None and budget < 0:
            raise ValueError("budget must be non-negative")

        # Private attributes
        self._history_ids: List[str] = []
        if history_ids:
            for hid in history_ids:
                if not isinstance(hid, str) or not hid.strip():
                    raise ValueError("each history id must be a non-empty string")
                self._history_ids.append(hid.strip())

        self._budget: Optional[float] = float(budget) if budget is not None else None
        self._token_weights: Dict[str, float] = {}

    # Properties
    @property
    def history_ids(self) -> List[str]:
        #list[str]: Copy of the user's selection history (read-only).
        return list(self._history_ids)

    @property
    def budget(self) -> Optional[float]:
        #float | None: User's non-negative budget or None.
        return self._budget

    @budget.setter
    def budget(self, value: Optional[float]) -> None:
        if value is None:
            self._budget = None
            return
        if not isinstance(value, (int, float)):
            raise TypeError("budget must be a number or None")
        if value < 0:
            raise ValueError("budget must be non-negative")
        self._budget = float(value)

    @property
    def token_weights(self) -> Dict[str, float]:
        #dict[str, float]: Copy of learned flavor/diet token weights (0..1).
        return dict(self._token_weights)

    # ---------- Methods ----------
    def add_meal_to_history(self, meal_id: str) -> None:
        """Add a meal ID to the user's history.

        Args:
            meal_id (str): Meal identifier to record.

        Raises:
            ValueError: If meal_id is empty.
        """
        if not isinstance(meal_id, str) or not meal_id.strip():
            raise ValueError("meal_id must be a non-empty string")
        self._history_ids.append(meal_id.strip())

    def update_preferences(self, meals: Iterable[Dict]) -> None:
        """Update learned token weights from the user's meal history.

        Args:
            meals (iterable of dict): Menu of meals, each with 'id', 'flavor', 'diet'.

        Raises:
            TypeError: If meals is not iterable.
        """
        if meals is None:
            raise TypeError("meals must be provided")
        self._token_weights = learn_preferences_from_history(meals, self._history_ids)

    def check_budget(self, price: float) -> bool:
        """Check if a meal price is within the user's budget.

        Args:
            price (float): Price of the meal.

        Returns:
            True if price <= budget or budget is None, else False.

        Raises:
            TypeError: If price is not a number.
            ValueError: If price is negative.
        """
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price < 0:
            raise ValueError("price must be non-negative")
        if self._budget is None:
            return True
        return within_budget(price, self._budget)

    def reset_history(self) -> None:
        #Clear the user's meal history.
        self._history_ids.clear()

    def reset_token_weights(self) -> None:
        #Clear the user's learned token weights.
        self._token_weights.clear()

    # String Representations
    def __str__(self) -> str:
        budget_str = f"${self._budget:.2f}" if self._budget is not None else "No budget"
        return f"UserPreferences(history={self._history_ids}, budget={budget_str})"

    def __repr__(self) -> str:
        return f"UserPreferences(history_ids={self._history_ids}, budget={self._budget})"

