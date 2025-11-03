from __future__ import annotations
from typing import Dict, List, Optional, Iterable



class UserPreferences:
    """Represents a user's meal preferences (history + budget + learned weights).

    Learns simple token weights from the user's selection history using
    tokens exposed by `Meal.tokens()` 

    Example:
        >>> # setup
        >>> m1 = Meal("1", "Spicy Tofu", 10.0, 450, "vegetarian", "spicy, savory")
        >>> m2 = Meal("2", "Chicken Curry", 12.0, 650, "meat", "spicy")
        >>> menu = Menu([m1, m2])
        >>> prefs = UserPreferences(history_ids=["1"], budget=11.0)
        >>> prefs.update_preferences(menu)
        >>> prefs.check_budget(10.5)
        True
        >>> prefs.check_budget(12.0)
        False
        >>> sorted(prefs.token_weights.items())  # doctest: +ELLIPSIS
        [...]
    """

    def __init__(self, history_ids: Optional[List[str]] = None, budget: Optional[float] = None) -> None:
        """Initialize preferences.

        Args:
            history_ids (list[str] | None): Prior selected meal ids.
            budget (float | None): Optional non-negative spending cap.

        Raises:
            TypeError: If types are invalid.
            ValueError: If budget is negative or ids are blank.
        """
        if history_ids is not None and not isinstance(history_ids, list):
            raise TypeError("history_ids must be a list[str] or None")
        if budget is not None and not isinstance(budget, (int, float)):
            raise TypeError("budget must be a number or None")
        if budget is not None and float(budget) < 0:
            raise ValueError("budget must be non-negative")

        # Private state
        self._history_ids: List[str] = []
        if history_ids:
            for hid in history_ids:
                if not isinstance(hid, str) or not hid.strip():
                    raise ValueError("each history id must be a non-empty string")
                self._history_ids.append(hid.strip())

        self._budget: Optional[float] = float(budget) if budget is not None else None
        self._token_weights: Dict[str, float] = {}

    # ---------- Properties (encapsulation) ----------
    @property
    def history_ids(self) -> List[str]:
        """list[str]: Copy of the user's selection history (read-only)."""
        return list(self._history_ids)

    @property
    def budget(self) -> Optional[float]:
        """float | None: Non-negative budget or None."""
        return self._budget

    @budget.setter
    def budget(self, value: Optional[float]) -> None:
        if value is None:
            self._budget = None
            return
        if not isinstance(value, (int, float)):
            raise TypeError("budget must be a number or None")
        if float(value) < 0:
            raise ValueError("budget must be non-negative")
        self._budget = float(value)

    @property
    def token_weights(self) -> Dict[str, float]:
        """dict[str, float]: Copy of learned token weights in [0,1]."""
        return dict(self._token_weights)

    # ---------- Public methods ----------
    def add_meal_to_history(self, meal_id: str, *, menu: Optional["Menu"] = None, require_exists: bool = False) -> None:
        """Append a meal id to history (optionally verifying it exists in the Menu).

        Args:
            meal_id (str): The meal identifier to record.
            menu (Menu | None): If provided, used to verify existence.
            require_exists (bool): If True, raise if meal_id not f
