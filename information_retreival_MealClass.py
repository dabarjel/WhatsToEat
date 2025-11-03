from typing import List, Optional
import csv
import statistics

class Meal:
    """ Represents a single meal with name, price, calories, diet, and flavor.

    Example:
        m = Meal("M1", "Tofu Bowl", 9.99, 450, "vegetarian", "savory")
        m.add_rating(5)
        m.add_rating(4)
        print(m.average_rating)
            4.5
    """

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str):
        # Validate input types and values
        if not all(isinstance(arg, str) for arg in [meal_id, name, diet, flavor]):
            raise TypeError("Meal id, name, diet, and flavor must be strings.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(calories, (int, float)) or calories < 0:
            raise ValueError("Calories must be non-negative.")

        # Initialize private attributes
        self._id = meal_id
        self._name = name.strip()
        self._price = float(price)
        self._calories = int(calories)
        self._diet = diet.strip()
        self._flavor = flavor.strip()
        self._ratings: List[int] = []

    # Properties (private attributes with safe access)
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float):
        if not isinstance(new_price, (int, float)) or new_price < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = float(new_price)

    @property
    def diet(self) -> str:
        #Return diet string (read-only property for encapsulation).
        return self._diet

    # Instance methods 
    def add_rating(self, rating: int) -> None:
        #Add a rating (1–5) to this meal.
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        self._ratings.append(rating)

    @property
    def average_rating(self) -> float:
        #Return the average rating or 0 if none.
        return float(statistics.mean(self._ratings)) if self._ratings else 0.0

    def format_meal(self) -> str:
        """Return a formatted one-line description of the meal."""
        return f"{self._name} (id:{self._id}) — ${self._price:.2f}, {self._calories} kcal"

    # String representations
    def __str__(self):
        return self.format_meal()

    def __repr__(self):
        return (f"Meal(id={self._id!r}, name={self._name!r}, price={self._price}, "
                f"calories={self._calories})")
