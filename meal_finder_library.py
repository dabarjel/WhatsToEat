"""
WhatsToEat function library for our meal suggestion project.

15 functions:
- Simple (5): small helpers and validations
- Medium (6): parsing, filtering, rating helpers
- Complex (4): scoring, recommending, analytics, learning preferences

"""

from typing import Any, Dict, Iterable, List, Optional, Tuple
import csv
import random
import statistics

Meal = Dict[str, Any]  # A meal is represented as a dictionary with known keys
RatingsDB = Dict[str, List[int]]  # meal_id -> list of rating ints (1..5)


# SIMPLE FUNCTIONS (5-10 lines each)

def normalize_text(text: str) -> str:
    """Normalize text for comparison: strip whitespace, lower-case, collapse spaces.

    Args:
        text: input string

    Returns:
        Normalized string

    Raises:
        TypeError: if input is not a string
    """
    if not isinstance(text, str):
        raise TypeError("normalize_text: text must be a string")
    # strip ends, lower-case, and collapse multiple spaces
    return " ".join(text.strip().lower().split())


def within_budget(price: float, budget: float) -> bool:
    """Return True if price is less than or equal to budget.

    Args:
        price: meal price
        budget: user's budget

    Returns:
        True if price <= budget

    Raises:
        TypeError: if inputs are not numbers
        ValueError: if price or budget are negative
    """
    if not isinstance(price, (int, float)) or not isinstance(budget, (int, float)):
        raise TypeError("within_budget: price and budget must be numbers")
    if price < 0 or budget < 0:
        raise ValueError("within_budget: price and budget must be non-negative")
    return float(price) <= float(budget)


def format_meal(meal: Meal) -> str:
    """Return a short human-readable string for a meal.

    Args:
        meal: dict with keys 'id', 'name', 'price', optionally 'calories'

    Returns:
        A one-line string describing the meal

    Raises:
        TypeError/ValueError if meal missing expected fields
    """
    if not isinstance(meal, dict):
        raise TypeError("format_meal: meal must be a dict")
    if "id" not in meal or "name" not in meal or "price" not in meal:
        raise ValueError("format_meal: meal must have 'id', 'name', and 'price' keys")
    price = meal["price"]
    try:
        price_val = float(price)
    except Exception:
        raise ValueError("format_meal: meal['price'] must be a number")
    calories = meal.get("calories", "?")
    return f"{meal['name']} (id:{meal['id']}) — ${price_val:.2f}, {calories} kcal"


def average_price(meals: Iterable[Meal]) -> float:
    """Return the average price of a list of meals (0 if no meals).

    Args:
        meals: iterable of meal dicts

    Returns:
        average price (float)

    Raises:
        TypeError if meals not iterable
    """
    if meals is None:
        raise TypeError("average_price: meals must be provided")
    prices = []
    for m in meals:
        if not isinstance(m, dict):
            continue
        p = m.get("price")
        if isinstance(p, (int, float)):
            prices.append(float(p))
    return float(statistics.mean(prices)) if prices else 0.0


def count_vegetarian(meals: Iterable[Meal]) -> int:
    """Count how many meals are vegetarian.

    Args:
        meals: iterable of meal dicts (must have 'diet' key containing string)

    Returns:
        integer count of vegetarian meals

    Raises:
        TypeError if meals not iterable
    """
    if meals is None:
        raise TypeError("count_vegetarian: meals must be provided")
    count = 0
    for m in meals:
        if not isinstance(m, dict):
            continue
        diet = m.get("diet", "")
        if not isinstance(diet, str):
            continue
        if "vegetarian" in diet.lower():
            count += 1
    return count


# MEDIUM FUNCTIONS (15-25 lines)

def parse_menu_csv(csv_text: str) -> List[Meal]:
    """Parse a CSV string into a list of meal dictionaries.

    Expected columns (at least): id,name,price,calories,diet,flavor
    diet and flavor are plain strings (e.g., "vegetarian", "spicy").

    Args:
        csv_text: CSV content as a string

    Returns:
        list of meal dicts

    Raises:
        TypeError: if csv_text not a string
        ValueError: if required columns missing
    """
    if not isinstance(csv_text, str):
        raise TypeError("parse_menu_csv: csv_text must be a string")
    lines = csv_text.strip().splitlines()
    if not lines:
        return []
    reader = csv.DictReader(lines)
    required = {"id", "name", "price", "calories", "diet", "flavor"}
    if not required.issubset(set(reader.fieldnames or [])):
        missing = required - set(reader.fieldnames or [])
        raise ValueError(f"parse_menu_csv: CSV missing columns: {missing}")
    meals: List[Meal] = []
    for row in reader:
        try:
            meal = {
                "id": str(row["id"]).strip(),
                "name": str(row["name"]).strip(),
                "price": float(row["price"]),
                "calories": int(float(row["calories"])),
                "diet": str(row["diet"]).strip(),
                "flavor": str(row["flavor"]).strip(),
                # optional fields:
                "ratings": [],  # start with empty ratings
            }
            meals.append(meal)
        except Exception:
            # skip rows that cannot be parsed rather than failing fully
            continue
    return meals


def filter_by_diet(meals: Iterable[Meal], restriction: str) -> List[Meal]:
    """Return meals that match a dietary restriction (case-insensitive substring).

    Args:
        meals: iterable of meal dicts
        restriction: diet restriction like 'vegetarian' or 'gluten-free'

    Returns:
        list of matching meal dicts

    Raises:
        TypeError if restriction not a string
    """
    if not isinstance(restriction, str):
        raise TypeError("filter_by_diet: restriction must be a string")
    key = restriction.lower().strip()
    result = []
    for m in meals:
        if not isinstance(m, dict):
            continue
        diet = m.get("diet", "")
        if not isinstance(diet, str):
            continue
        if key in diet.lower():
            result.append(m)
    return result


def filter_by_price(meals: Iterable[Meal], max_price: float) -> List[Meal]:
    """Return meals at or below max_price.

    Args:
        meals: iterable of meal dicts
        max_price: price threshold

    Returns:
        list of affordable meals

    Raises:
        TypeError/ValueError for bad inputs
    """
    if not isinstance(max_price, (int, float)):
        raise TypeError("filter_by_price: max_price must be a number")
    if max_price < 0:
        raise ValueError("filter_by_price: max_price must be non-negative")
    result = []
    for m in meals:
        if not isinstance(m, dict):
            continue
        p = m.get("price")
        if isinstance(p, (int, float)) and float(p) <= float(max_price):
            result.append(m)
    return result


def add_rating(meal: Meal, rating: int) -> None:
    """Add a rating (1..5) to the meal's 'ratings' list (in-place).

    Args:
        meal: meal dict (will be modified)
        rating: integer 1..5

    Raises:
        TypeError/ValueError for bad inputs
    """
    if not isinstance(meal, dict):
        raise TypeError("add_rating: meal must be a dict")
    if not isinstance(rating, int):
        raise TypeError("add_rating: rating must be an int")
    if rating < 1 or rating > 5:
        raise ValueError("add_rating: rating must be between 1 and 5")
    if "ratings" not in meal or not isinstance(meal["ratings"], list):
        meal["ratings"] = []
    meal["ratings"].append(rating)


def get_average_rating(meal: Meal) -> float:
    """Return the average rating for a meal (0 if no ratings).

    Args:
        meal: meal dict

    Returns:
        average rating as float

    Raises:
        TypeError if meal invalid
    """
    if not isinstance(meal, dict):
        raise TypeError("get_average_rating: meal must be a dict")
    r = meal.get("ratings", [])
    if not isinstance(r, list) or not r:
        return 0.0
    valid_ratings = [x for x in r if isinstance(x, int) and 1 <= x <= 5]
    return float(statistics.mean(valid_ratings)) if valid_ratings else 0.0


def suggest_by_flavor(meals: Iterable[Meal], flavor: str, budget: Optional[float] = None) -> Optional[Meal]:
    """Suggest a random meal that matches flavor and (optionally) fits budget.

    Args:
        meals: iterable of meals
        flavor: flavor keyword (e.g., 'spicy')
        budget: optional budget to filter by

    Returns:
        a single meal dict or None if no match

    Raises:
        TypeError/ValueError for bad inputs
    """
    if not isinstance(flavor, str):
        raise TypeError("suggest_by_flavor: flavor must be a string")
    candidates = []
    for m in meals:
        if not isinstance(m, dict):
            continue
        if flavor.lower() in str(m.get("flavor", "")).lower():
            if budget is None:
                candidates.append(m)
            else:
                p = m.get("price")
                if isinstance(p, (int, float)) and float(p) <= float(budget):
                    candidates.append(m)
    return random.choice(candidates) if candidates else None


# COMPLEX FUNCTIONS (30+ lines each, but still simple logic)

def learn_preferences_from_history(meals: Iterable[Meal], history_ids: Iterable[str]) -> Dict[str, float]:
    """Learn simple preference weights for flavor/diet tokens from user history.

    For each meal id in history_ids, find the meal in meals and count occurrences
    of its flavor and diet tokens. Return normalized weights 0..1 per token.

    Args:
        meals: iterable of meal dicts (must include 'id', 'flavor', 'diet')
        history_ids: iterable of meal ids representing user's past selections

    Returns:
        dict mapping token -> normalized weight (float)

    Raises:
        TypeError for bad inputs
    """
    if meals is None or history_ids is None:
        raise TypeError("learn_preferences_from_history: meals and history_ids must be provided")
    # Build id -> meal map for quick lookup
    meal_map = {}
    for m in meals:
        if isinstance(m, dict) and "id" in m:
            meal_map[str(m["id"])] = m
    token_counts: Dict[str, int] = {}
    total = 0
    # For each id in the history, extract tokens from the meal's flavor/diet
    for hid in history_ids:
        if hid is None:
            continue
        hid_s = str(hid)
        meal = meal_map.get(hid_s)
        if not meal:
            continue
        # split flavor and diet into simple tokens by commas or spaces
        flavor = str(meal.get("flavor", "")).lower()
        diet = str(meal.get("diet", "")).lower()
        tokens = []
        for part in (flavor.split(",") + diet.split(",")):
            for token in part.strip().split():
                t = token.strip()
                if t:
                    tokens.append(t)
        # count tokens
        for t in tokens:
            token_counts[t] = token_counts.get(t, 0) + 1
            total += 1
    if total == 0:
        return {}
    # normalize counts to weights between 0 and 1
    return {k: v / total for k, v in token_counts.items()}


def compute_relevance_score(meal: Meal, prefs: Dict[str, float], budget: Optional[float] = None) -> float:
    """Compute a relevance score for a single meal given user preference weights.

    Score components:
    - token match: sum of prefs weights for tokens present (flavor/diet tokens)
    - rating bonus: average rating (0..5) adds directly
    - budget proximity: slight bonus if meal <= budget, penalty if much over budget

    Args:
        meal: meal dict
        prefs: dict token -> weight (from learn_preferences_from_history)
        budget: optional budget to bias scoring

    Returns:
        float relevance score (higher is better)

    Raises:
        TypeError/ValueError for invalid inputs
    """
    if not isinstance(meal, dict):
        raise TypeError("compute_relevance_score: meal must be a dict")
    if not isinstance(prefs, dict):
        raise TypeError("compute_relevance_score: prefs must be a dict")
    # Token matching
    flavor = str(meal.get("flavor", "")).lower()
    diet = str(meal.get("diet", "")).lower()
    tokens = set()
    for part in (flavor.split(",") + diet.split(",")):
        for token in part.strip().split():
            t = token.strip()
            if t:
                tokens.add(t)
    token_score = 0.0
    for t in tokens:
        token_score += float(prefs.get(t, 0.0))
    # Rating contribution
    rating_avg = get_average_rating(meal)  # 0..5
    # Budget effect
    budget_effect = 0.0
    if budget is not None:
        if not isinstance(budget, (int, float)):
            raise TypeError("compute_relevance_score: budget must be a number or None")
        price = meal.get("price")
        if isinstance(price, (int, float)):
            if float(price) <= float(budget):
                # small bonus: the closer to budget (but <=) the slightly higher
                budget_effect += max(0.0, 1.0 - ((float(budget) - float(price)) / max(1.0, float(budget)))) * 0.5
            else:
                # penalty for being above budget
                budget_effect -= (float(price) - float(budget)) * 0.2
    # Final score: weighted sum
    score = token_score * 2.0 + rating_avg + budget_effect
    return float(score)


def recommend_meals(
    meals: Iterable[Meal],
    prefs: Optional[Dict[str, float]] = None,
    budget: Optional[float] = None,
    top_k: int = 3,
    strategy: str = "best",
    rng: Optional[random.Random] = None
) -> List[Meal]:
    """Recommend meals using one of three strategies: 'best', 'random', 'hybrid'.

    - 'best': compute relevance score for each meal and return top_k by score
    - 'random': return top_k random meals (filtered by budget if provided)
    - 'hybrid': return a mix of top scoring and some random choices

    Args:
        meals: iterable of meal dicts
        prefs: preference weights (token -> float)
        budget: optional budget to filter/penalize
        top_k: number of meals to return (must be >=1)
        strategy: 'best', 'random', or 'hybrid'
        rng: optional random.Random instance for deterministic results (tests)

    Returns:
        list of up to top_k recommended meal dicts

    Raises:
        ValueError/TypeError for bad inputs
    """
    if not isinstance(top_k, int) or top_k < 1:
        raise ValueError("recommend_meals: top_k must be an int >= 1")
    if strategy not in {"best", "random", "hybrid"}:
        raise ValueError("recommend_meals: strategy must be 'best', 'random', or 'hybrid'")
    rng = rng or random.Random()
    prefs = prefs or {}

    # Collect candidate meals, validating basic structure and optionally filtering by budget
    candidates: List[Meal] = []
    for m in meals:
        if not isinstance(m, dict):
            continue
        if "id" not in m or "name" not in m or "price" not in m:
            continue
        # optional quick budget filter (still scored penalizes above budget)
        if budget is not None:
            p = m.get("price")
            if isinstance(p, (int, float)) and float(p) > float(budget):
                # keep it but it will be penalized in scoring; we still include so hybrid/random can see variety
                candidates.append(m)
            else:
                candidates.append(m)
        else:
            candidates.append(m)

    if not candidates:
        return []

    if strategy == "random":
        # unbiased random picks (unique)
        picks = []
        pool = list(candidates)
        while pool and len(picks) < top_k:
            pick = rng.choice(pool)
            picks.append(pick)
            pool.remove(pick)
        return picks

    # For 'best' and 'hybrid' compute scores
    scored: List[Tuple[float, Meal]] = []
    for m in candidates:
        try:
            s = compute_relevance_score(m, prefs, budget)
        except Exception:
            s = -9999.0
        scored.append((s, m))
    # sort descending by score
    scored.sort(key=lambda x: x[0], reverse=True)

    if strategy == "best":
        return [m for _, m in scored[:top_k]]

    # hybrid: take top half by score, plus some random picks from the remainder
    half = max(1, len(scored) // 2)
    top_half = [m for _, m in scored[:half]]
    picks = top_half[:max(1, min(top_k, len(top_half)) // 2)]
    remaining = [m for _, m in scored if m not in picks]
    while len(picks) < top_k and remaining:
        pick = rng.choice(remaining)
        picks.append(pick)
        remaining.remove(pick)
    return picks


def generate_analytics(meals: Iterable[Meal], top_n: int = 3) -> Dict[str, Any]:
    """Compute simple analytics:
    - top_rated: list of top_n meals by average rating
    - avg_price: overall average price
    - price_range: min and max price
    - flavor_counts: how many meals per flavor token

    Args:
        meals: iterable of meal dicts
        top_n: how many top-rated meals to return

    Returns:
        dict with analytics results

    Raises:
        TypeError/ValueError for bad inputs
    """
    if meals is None:
        raise TypeError("generate_analytics: meals must be provided")
    if not isinstance(top_n, int) or top_n < 1:
        raise ValueError("generate_analytics: top_n must be int >= 1")

    meal_list = [m for m in meals if isinstance(m, dict)]
    # compute average rating per meal and store pairs
    rated_pairs: List[Tuple[float, Meal]] = []
    prices = []
    flavor_counts: Dict[str, int] = {}
    for m in meal_list:
        p = m.get("price")
        if isinstance(p, (int, float)):
            prices.append(float(p))
        avg = get_average_rating(m)
        if avg > 0:
            rated_pairs.append((avg, m))
        flavor = str(m.get("flavor", "")).lower()
        # split by comma and whitespace
        for part in flavor.split(","):
            for token in part.strip().split():
                t = token.strip()
                if t:
                    flavor_counts[t] = flavor_counts.get(t, 0) + 1

    rated_pairs.sort(key=lambda x: x[0], reverse=True)
    top_rated = [{"id": m["id"], "name": m.get("name", ""), "avg_rating": avg} for avg, m in rated_pairs[:top_n]]

    analytics = {
        "top_rated": top_rated,
        "avg_price": float(statistics.mean(prices)) if prices else 0.0,
        "min_price": float(min(prices)) if prices else None,
        "max_price": float(max(prices)) if prices else None,
        "flavor_counts": flavor_counts,
        "total_meals": len(meal_list),
    }
    return analytics
