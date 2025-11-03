from __future__ import annotations
from typing import Iterable, List, Tuple, Dict, Optional
import csv
import statistics



class Menu:
    """Collection of Meal objects with search and stats.

    Integrates Project 1 functions by tokenizing and ranking items for
    simple information-retrieval-style search.

    Example:
        >>> csv_text = "id,name,price,calories,diet,flavor\\n1,Pasta,12.5,550,vegetarian,creamy"
        >>> menu, errs = Menu.from_csv(csv_text)
        >>> errs
        []
        >>> round(menu.average_price(), 2)
        12.5
        >>> len(menu.search("creamy vegetarian", top_k=1))  # doctest: +ELLIPSIS
        1
    """

    def __init__(self, meals: Optional[Iterable["Meal"]] = None):
        """Initialize Menu.

        Args:
            meals (Iterable[Meal] | None): Optional iterable of Meal instances.

        Raises:
            TypeError: If any element is not a Meal.
        """
        self._meals: List["Meal"] = []
        if meals is not None:
            for m in meals:
                if not hasattr(m, "__class__") or m.__class__.__name__ != "Meal":
                    # Avoid circular import in type check; prefer duck-typing or isinstance if Meal is importable.
                    raise TypeError("All items must be Meal instances.")
                self._meals.append(m)

    # ---------- Encapsulation ----------
    @property
    def meals(self) -> List["Meal"]:
        """list[Meal]: Copy of meals (read-only to callers)."""
        return list(self._meals)

    # Basic mutators with validation
    def add(self, meal: "Meal") -> None:
        """Add a Meal (no duplicates by id)."""
        if meal is None or meal.__class__.__name__ != "Meal":
            raise TypeError("meal must be a Meal instance.")
        if any(m.id == meal.id for m in self._meals):
            raise ValueError(f"Meal with id '{meal.id}' already exists.")
        self._meals.append(meal)

    def add_many(self, meals: Iterable["Meal"]) -> None:
        """Add many meals; raises if any id duplicates."""
        ids = {m.id for m in self._meals}
        for m in meals:
            if m.__class__.__name__ != "Meal":
                raise TypeError("All items must be Meal instances.")
            if m.id in ids:
                raise ValueError(f"Duplicate id '{m.id}' in add_many.")
            ids.add(m.id)
            self._meals.append(m)

    def remove(self, meal_id: str) -> Optional["Meal"]:
        """Remove by id; returns removed Meal or None."""
        for i, m in enumerate(self._meals):
            if m.id == meal_id:
                return self._meals.pop(i)
        return None

    def get(self, meal_id: str) -> Optional["Meal"]:
        """Get by id or None."""
        for m in self._meals:
            if m.id == meal_id:
                return m
        return None

    # ---------- Alternate constructor (CSV) ----------
    @classmethod
    def from_csv(cls, csv_text: str) -> Tuple["Menu", List[str]]:
        """Parse CSV text into a Menu and a list of row-level error messages.

        Required headers: id, name, price, calories, diet, flavor

        Args:
            csv_text (str): CSV string with header row.

        Returns:
            (Menu, list[str]): The built menu and any parsing errors.

        Raises:
            TypeError: If csv_text is not a string.
            ValueError: If required headers are missing.
        """
        if not isinstance(csv_text, str):
            raise TypeError("Menu.from_csv: csv_text must be a string")
        lines = [ln for ln in csv_text.strip().splitlines() if ln.strip()]
        reader = csv.DictReader(lines)
        required = {"id", "name", "price", "calories", "diet", "flavor"}
        if reader.fieldnames is None or not required.issubset({h.strip() for h in reader.fieldnames}):
            raise ValueError(f"CSV missing required headers: {sorted(required)}")

        meals: List["Meal"] = []
        errors: List[str] = []
        rownum = 1  # header is row 1 for user-friendly messages
        for row in reader:
            rownum += 1
            try:
                m = Meal(
                    meal_id=str(row["id"]).strip(),
                    name=str(row["name"]).strip(),
                    price=float(row["price"]),
                    calories=int(float(row["calories"])),
                    diet=str(row["diet"]).strip(),
                    flavor=str(row["flavor"]).strip(),
                )
                meals.append(m)
            except Exception as exc:
                errors.append(f"Row {rownum}: {exc!s}")
        return cls(meals), errors

    # ---------- Core filters & stats ----------
    def filter_by_diet(self, restriction: str) -> List["Meal"]:
        """Return meals matching a dietary restriction (case-insensitive)."""
        if not isinstance(restriction, str):
            raise TypeError("restriction must be a string.")
        key = restriction.lower().strip()
        return [m for m in self._meals if key in m.diet.lower()]

    def filter_by_price(self, max_price: float) -> List["Meal"]:
        """Return meals at or below max_price."""
        if not isinstance(max_price, (int, float)) or max_price < 0:
            raise ValueError("max_price must be non-negative.")
        cap = float(max_price)
        return [m for m in self._meals if m.price <= cap]

    def average_price(self) -> float:
        """Average price of all meals in menu (0.0 if empty)."""
        prices = [m.price for m in self._meals]
        return float(statistics.mean(prices)) if prices else 0.0

    def count_vegetarian(self) -> int:
        """Count meals that include 'vegetarian' in diet."""
        return sum(1 for m in self._meals if "vegetarian" in m.diet.lower())

    # ---------- Project 1 integration ----------
    def as_tokens_map(self) -> Dict[str, List[str]]:
        """Return {meal_id: tokens} using Meal.tokens() (P1 tokenize)."""
        return {m.id: m.tokens() for m in self._meals}

    def search(self, text: str, top_k: int = 5) -> List["Meal"]:
        """Search meals by text using P1 tokenize + rank_results.

        Args:
            text (str): Query text.
            top_k (int): Number of results to return (>=1).

        Returns:
            list[Meal]: Top-k meals ranked by overlap.

        Raises:
            TypeError: If text is not a string.
            ValueError: If top_k < 1.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string.")
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be an int >= 1.")

        # q_tokens = p1.tokenize(text)
        # scores = p1.rank_results(q_tokens, self.as_tokens_map())
        # --- Replace the two lines above with your Project 1 functions. ---
        q_tokens = [t.lower() for t in text.split() if t.strip()]
        docs = self.as_tokens_map()
        scores = {k: len(set(q_tokens) & set(v)) for k, v in docs.items()}  # simple fallback

        ranked_ids = sorted(scores, key=scores.get, reverse=True)[:top_k]
        id_to_meal = {m.id: m for m in self._meals}
        return [id_to_meal[mid] for mid in ranked_ids if mid in id_to_meal]

    # ---------- Magic methods ----------
    def __len__(self) -> int:
        return len(self._meals)

    def __iter__(self):
        return iter(self._meals)

    def __str__(self) -> str:
        return f"Menu with {len(self._meals)} meals"

    def __repr__(self) -> str:
        return f"Menu(n_meals={len(self._meals)})"
