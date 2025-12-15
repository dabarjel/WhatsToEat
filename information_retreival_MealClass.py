from typing import List, Optional, Dict, Any
import statistics
from meal_finder_library import add_rating, get_average_rating, format_meal

class Meal:
    """Represents a single meal using the function library for ratings and formatting.

    Example:
        m = Meal("M1", "Tofu Bowl", 9.99, 450, "vegetarian", "savory")
        m.add_rating(5)
        m.add_rating(4)
        print(m.average_rating)  # 4.5
        print(m.format_meal())   # Tofu Bowl (id:M1) — $9.99, 450 kcal
    """

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str):
        # Validate basic types
        if not all(isinstance(arg, str) for arg in [meal_id, name, diet, flavor]):
            raise TypeError("Meal id, name, diet, and flavor must be strings.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(calories, (int, float)) or calories < 0:
            raise ValueError("Calories must be non-negative.")

        # Store all meal data in a dict to integrate with the function library
        self._meal_dict: Dict[str, Any] = {
            "id": meal_id.strip(),
            "name": name.strip(),
            "price": float(price),
            "calories": int(calories),
            "diet": diet.strip(),
            "flavor": flavor.strip(),
            "ratings": []
        }

    # Properties
    @property
    def id(self) -> str:
        return self._meal_dict["id"]

    @property
    def name(self) -> str:
        return self._meal_dict["name"]

    @property
    def price(self) -> float:
        return self._meal_dict["price"]

    @price.setter
    def price(self, new_price: float):
        if not isinstance(new_price, (int, float)) or new_price < 0:
            raise ValueError("Price must be a non-negative number.")
        self._meal_dict["price"] = float(new_price)

    @property
    def calories(self) -> int:
        return self._meal_dict["calories"]

    @property
    def diet(self) -> str:
        return self._meal_dict["diet"]

    @property
    def flavor(self) -> str:
        return self._meal_dict["flavor"]

    # Methods integrating function library
    def add_rating(self, rating: int) -> None:
        #Add a rating to this meal (1–5).
        add_rating(self._meal_dict, rating)

    @property
    def average_rating(self) -> float:
        #Return the average rating for this meal (0 if no ratings).
        return get_average_rating(self._meal_dict)

    def format_meal(self) -> str:
        #Return a formatted one-line description using library function.
        return format_meal(self._meal_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return dictionary representation of meal."""
        result = dict(self._meal_dict)
        result['type'] = 'standard'  # Add type for meal_from_dict compatibility
        return result

    # String representations
    def __str__(self):
        return self.format_meal()

    def __repr__(self):
        return (f"Meal(id={self.id!r}, name={self.name!r}, price={self.price}, "
                f"calories={self.calories}, diet={self.diet!r}, flavor={self.flavor!r})")
