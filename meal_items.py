"""Meal item classes with inheritance hierarchy."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from meal_finder_library import add_rating, get_average_rating, format_meal


class AbstractMealItem(ABC):
    """Base class for all meal items."""

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str):
        self._meal_dict: Dict[str, Any] = {
            "id": meal_id,
            "name": name,
            "price": float(price),
            "calories": int(calories),
            "diet": diet,
            "flavor": flavor,
            "ratings": []
        }

    @property
    def id(self) -> str:
        return self._meal_dict["id"]

    @property
    def name(self) -> str:
        return self._meal_dict["name"]

    @property
    def price(self) -> float:
        return self._meal_dict["price"]

    @property
    def calories(self) -> int:
        return self._meal_dict["calories"]

    @property
    def diet(self) -> str:
        return self._meal_dict["diet"]

    @property
    def flavor(self) -> str:
        return self._meal_dict["flavor"]

    def add_rating(self, rating: int) -> None:
        add_rating(self._meal_dict, rating)

    @property
    def average_rating(self) -> float:
        return get_average_rating(self._meal_dict)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._meal_dict)

    @abstractmethod
    def calculate_value_score(self) -> float:
        """Calculate value score for this meal type."""
        pass

    @abstractmethod
    def get_preparation_info(self) -> str:
        """Get preparation information."""
        pass


class StandardMeal(AbstractMealItem):
    """Regular meal with standard preparation."""

    def calculate_value_score(self) -> float:
        calories_per_dollar = self.calories / max(self.price, 0.01)
        rating_bonus = self.average_rating * 2
        return calories_per_dollar + rating_bonus

    def get_preparation_info(self) -> str:
        return "Standard preparation: 15-20 minutes"


class SpecialtyMeal(AbstractMealItem):
    """Premium meal with extended preparation time."""

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str,
                 preparation_time: int = 30):
        super().__init__(meal_id, name, price, calories, diet, flavor)
        self._meal_dict["preparation_time"] = preparation_time

    @property
    def preparation_time(self) -> int:
        return self._meal_dict["preparation_time"]

    def calculate_value_score(self) -> float:
        rating_score = self.average_rating * 5
        time_penalty = self.preparation_time / 100
        return rating_score - time_penalty

    def get_preparation_info(self) -> str:
        return f"Chef-prepared: {self.preparation_time} minutes"


class BundleMeal(AbstractMealItem):
    """Combo meal with discount."""

    def __init__(self, meal_id: str, name: str, price: float,
                 calories: int, diet: str, flavor: str,
                 num_items: int = 2, discount_percent: float = 20.0):
        super().__init__(meal_id, name, price, calories, diet, flavor)
        self._meal_dict["num_items"] = num_items
        self._meal_dict["discount_percent"] = discount_percent

    @property
    def num_items(self) -> int:
        return self._meal_dict["num_items"]

    @property
    def discount_percent(self) -> float:
        return self._meal_dict["discount_percent"]

    def calculate_value_score(self) -> float:
        discount_score = self.discount_percent * 2
        variety_bonus = self.num_items * 3
        rating_bonus = self.average_rating * 2
        return discount_score + variety_bonus + rating_bonus

    def get_preparation_info(self) -> str:
        return f"Bundle of {self.num_items} items: {self.discount_percent}% off"

def meal_from_dict(data: dict) -> AbstractMealItem:
    """
    Factory function to create the correct Meal object from a dictionary.
    """

    meal_type = data.get("type")

    if meal_type == "standard":
        return StandardMeal(
            meal_id=data["id"],
            name=data["name"],
            price=data["price"],
            calories=data["calories"],
            diet=data["diet"],
            flavor=data["flavor"]
        )

    if meal_type == "specialty":
        return SpecialtyMeal(
            meal_id=data["id"],
            name=data["name"],
            price=data["price"],
            calories=data["calories"],
            diet=data["diet"],
            flavor=data["flavor"],
            preparation_time=data.get("preparation_time", 30)
        )

    if meal_type == "bundle":
        return BundleMeal(
            meal_id=data["id"],
            name=data["name"],
            price=data["price"],
            calories=data["calories"],
            diet=data["diet"],
            flavor=data["flavor"],
            num_items=data.get("num_items", 2),
            discount_percent=data.get("discount_percent", 20.0)
        )

    raise ValueError(f"Unknown meal type: {meal_type}")

