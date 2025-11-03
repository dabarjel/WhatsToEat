from __future__ import annotations
from typing import Iterable, List, Tuple, Dict, Optional, Any
from meal_finder_library import (
    normalize_text,
    parse_menu_csv,
    filter_by_diet,
    filter_by_price,
    average_price,
    count_vegetarian,
    recommend_meals,
    generate_analytics
)

class Menu:
    """Collection of Meal objects with search, filtering, and analytics.

    Integrates WhatsToEat function library for parsing, filtering,
    scoring, and analytics.

    Example:
        >>> csv_text = "id,name,price,calories,diet,flavor\\n1,Pasta,12.5,550,vegetarian,creamy"
        >>> menu, errs = Menu.from_csv(csv_text)
        >>> errs
        []
        >>> round(menu.average_price(), 2)
        12.5
        >>> menu.filter_by_diet("vegetarian")[0].name
        'Pasta'
    """

    def __init__(self, meals: Optional[Iterable["Meal"]] = None):
        self._meals: List["Meal"] = []
        if meals is not None:
            for m in meals:
                if not hasattr(m, "__class__") or m.__class__.__name__ != "Meal":
                    raise TypeError("All items must be Meal instances.")
                self._meals.append(m)

    # Properties
    @property
    def meals(self) -> List["Meal"]:
        #Return a copy of meals (read-only).
        return list(self._meals)

    # Add / Remove
    def add(self, meal: "Meal") -> None:
        #Add a single Meal instance; raises if duplicate id.
        if meal is None or meal.__class__.__name__ != "Meal":
            raise TypeError("meal must be a Meal instance.")
        if any(m.id == meal.id for m in self._meals):
            raise ValueError(f"Meal with id '{meal.id}' already exists.")
        self._meals.append(meal)

    def add_many(self, meals: Iterable["Meal"]) -> None:
        #Add multiple meals; raises if any duplicates.
        ids = {m.id for m in self._meals}
        for m in meals:
            if m.__class__.__name__ != "Meal":
                raise TypeError("All items must be Meal instances.")
            if m.id in ids:
                raise ValueError(f"Duplicate id '{m.id}' in add_many.")
            ids.add(m.id)
            self._meals.append(m)

    def remove(self, meal_id: str) -> Optional["Meal"]:
        #Remove meal by id; return the removed meal or None.
        for i, m in enumerate(self._meals):
            if m.id == meal_id:
                return self._meals.pop(i)
        return None

    def get(self, meal_id: str) -> Optional["Meal"]:
        #Get meal by id; return None if not found.
        for m in self._meals:
            if m.id == meal_id:
                return m
        return None

    # Alternate constructor (CSV)
    @classmethod
    def from_csv(cls, csv_text: str) -> Tuple["Menu", List[str]]:
        #Parse CSV into Menu; returns list of parsing errors.
        try:
            meal_dicts = parse_menu_csv(csv_text)  # Library function
            meals = [Meal(**m) for m in meal_dicts]  # Convert dicts to Meal objects
            return cls(meals), []
        except Exception as exc:
            return cls([]), [str(exc)]

    # Filtering / Stats using library functions
    def filter_by_diet(self, restriction: str) -> List["Meal"]:
        #Return meals matching diet restriction.
        meal_dicts = [m.to_dict() for m in self._meals]
        filtered_dicts = filter_by_diet(meal_dicts, restriction)
        return [self.get(m["id"]) for m in filtered_dicts]

    def filter_by_price(self, max_price: float) -> List["Meal"]:
        #Return meals with price <= max_price.
        meal_dicts = [m.to_dict() for m in self._meals]
        filtered_dicts = filter_by_price(meal_dicts, max_price)
        return [self.get(m["id"]) for m in filtered_dicts]

    def average_price(self) -> float:
        #Return average price of all meals (0 if empty).
        return average_price([m.to_dict() for m in self._meals])

    def count_vegetarian(self) -> int:
        #Count meals labeled vegetarian.
        return count_vegetarian([m.to_dict() for m in self._meals])

    # Recommendation / Analytics
    def recommend(
        self,
        prefs: Optional[Dict[str, float]] = None,
        budget: Optional[float] = None,
        top_k: int = 5,
        strategy: str = "best"
    ) -> List["Meal"]:
        #Return top_k recommended meals using library recommend_meals.
        meal_dicts = [m.to_dict() for m in self._meals]
        recommended_dicts = recommend_meals(
            meal_dicts, prefs=prefs, budget=budget, top_k=top_k, strategy=strategy
        )
        return [self.get(m["id"]) for m in recommended_dicts]

    def analytics(self) -> Dict[str, Any]:
        #Return analytics dictionary using library generate_analytics.
        return generate_analytics([m.to_dict() for m in self._meals])
    # Magic methods
    def __len__(self) -> int:
        return len(self._meals)

    def __iter__(self):
        return iter(self._meals)

    def __str__(self):
        return f"Menu with {len(self._meals)} meals"

    def __repr__(self):
        return f"Menu(n_meals={len(self._meals)})"
