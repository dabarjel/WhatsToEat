from __future__ import annotations
from typing import List, Sequence
import statistics
# from project1 import normalize_text, tokenize
# or, if you made a shim/adapter:
# from .p1_compat import p1

class Meal:
    """Represents a single meal with name, price, calories, diet, and flavor.

    Integrates Project 1 functions by normalizing text fields and exposing
    tokenization for downstream ranking/search.

    Example:
        >>> m = Meal("M1", "  Tofu Bowl  ", 9.99, 450, "vegetarian", "spicy, savory")
        >>> m.add_rating(5); m.add_rating(4)
        >>> round(m.average_rating, 2)
        4.5
        >>> "spicy" in m.tokens()
        True
    """

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str):
        """Initialize a Meal.

        Args:
            meal_id (str): Unique identifier (non-empty).
            name (str): Display name (non-empty).
            price (float): Non-negative price.
            calories (int): Non-negative calories.
            diet (str): Diet tag(s), e.g., "vegetarian".
            flavor (str): Flavor keywords, e.g., "spicy, savory".

        Raises:
            TypeError: If parameter types are invalid.
            ValueError: If strings are empty/blank or numbers are negative.
        """
        # --- type checks
        if not isinstance(meal_id, str) or not isinstance(name, str) \
           or not isinstance(diet, str) or not isinstance(flavor, str):
            raise TypeError("meal_id, name, diet, and flavor must be strings.")
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number.")
        if not isinstance(calories, int):
            raise TypeError("calories must be an int.")

        # --- value checks
        if not meal_id.strip():
            raise ValueError("meal_id cannot be empty.")
        if not name.strip():
            raise ValueError("name cannot be empty.")
        if price < 0:
            raise ValueError("price must be non-negative.")
        if calories < 0:
            raise ValueError("calories must be non-negative.")
        if not diet.strip():
            raise ValueError("diet cannot be empty.")
        if not flavor.strip():
            raise ValueError("flavor cannot be empty.")

        # Initialize private attributes (normalize text fields via P1)
        self._id = meal_id.strip()
        # name/diet/flavor normalized using P1:
        self._name = self._normalize(name)
        self._price = float(price)
        self._calories = int(calories)
        self._diet = self._normalize(diet)
        self._flavor = self._normalize(flavor)
        self._ratings: List[float] = []

    # --------- Properties (encapsulation with validation) ---------
    @property
    def id(self) -> str:
        """str: Read-only meal id."""
        return self._id

    @property
    def name(self) -> str:
        """str: Meal name (normalized)."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        v = self._normalize(value)
        if not v:
            raise ValueError("name cannot be empty.")
        self._name = v

    @property
    def price(self) -> float:
        """float: Non-negative price."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        if not isinstance(new_price, (int, float)):
            raise TypeError("price must be a number.")
        if float(new_price) < 0:
            raise ValueError("price must be non-negative.")
        self._price = float(new_price)

    @property
    def calories(self) -> int:
        """int: Non-negative calories."""
        return self._calories

    @calories.setter
    def calories(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("calories must be an int.")
        if value < 0:
            raise ValueError("calories must be non-negative.")
        self._calories = value

    @property
    def diet(self) -> str:
        """str: Diet tag(s) (normalized)."""
        return self._diet

    @diet.setter
    def diet(self, value: str) -> None:
        v = self._normalize(value)
        if not v:
            raise ValueError("diet cannot be empty.")
        self._diet = v

    @property
    def flavor(self) -> str:
        """str: Flavor keywords (normalized)."""
        return self._flavor

    @flavor.setter
    def flavor(self, value: str) -> None:
        v = self._normalize(value)
        if not v:
            raise ValueError("flavor cannot be empty.")
        self._flavor = v

    @property
    def ratings(self) -> List[float]:
        """list[float]: Copy of ratings for read-only external access."""
        return list(self._ratings)

    # ----------------- Instance methods (3–5 total) -----------------
    def add_rating(self, rating: float) -> None:
        """Add a rating between 0 and 5 (inclusive).

        Raises:
            TypeError: If rating is not numeric.
            ValueError: If rating is outside [0, 5].
        """
        if not isinstance(rating, (int, float)):
            raise TypeError("rating must be a number.")
        r = float(rating)
        if not (0.0 <= r <= 5.0):
            raise ValueError("rating must be in [0, 5].")
        self._ratings.append(r)

    @property
    def average_rating(self) -> float:
        """float: Average rating, or 0.0 if none."""
        return float(statistics.mean(self._ratings)) if self._ratings else 0.0

    def tokens(self) -> list[str]:
        """Tokenize key text fields using Project 1 `tokenize`.

        Returns:
            list[str]: Lowercased tokens from name + diet + flavor.
        """
        blob = " ".join([self._name, self._diet, self._flavor]).strip()
        return self._tokenize(blob)

    def format_meal(self) -> str:
        """Return a formatted one-line description of the meal."""
        return f"{self._name} (id:{self._id}) — ${self._price:.2f}, {self._calories} kcal"

    # ----------------- String representations -----------------
    def __str__(self) -> str:
        return self.format_meal()

    def __repr__(self) -> str:
        return f"Meal(id={self._id!r}, name={self._name!r}, price={self._price!r}, calories={self._calories!r})"

    # ----------------- Private helpers (P1 integration points) -----------------
    @staticmethod
    def _normalize(text: str) -> str:
        # replace with your Project 1 normalize function:
        # return normalize_text(text)
        return " ".join(str(text).split()).strip()

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        # replace with your Project 1 tokenize function:
        # return tokenize(text)
        return [t.lower() for t in str(text).split() if t.strip()]
