# --- Simple UserPreferences class ---
class UserPreferences:
    """
    Represents a user's meal preferences.
    """

    def __init__(self, history_ids=None, budget=None):
        # validate inputs
        if history_ids is not None and not isinstance(history_ids, list):
            raise TypeError("history_ids must be a list or None")
        if budget is not None:
            if not isinstance(budget, (int, float)):
                raise TypeError("budget must be a number or None")
            if budget < 0:
                raise ValueError("budget must be non-negative")
        # store history and budget
        self.history_ids = list(history_ids) if history_ids else []
        self.budget = budget
        # stores token weights learned from history
        self.token_weights = {}

    def update_preferences(self, meals):
        """
        Learn simple preference weights from history meals.
        """
        if meals is None or not hasattr(meals, "__iter__"):
            raise TypeError("meals must be an iterable of meal dictionaries")
        token_counts = {}  # count occurrences of each flavor/diet token
        total = 0  # total tokens counted
        # map meal IDs to meal dicts for quick lookup
        meal_map = {m['id']: m for m in meals if isinstance(m, dict) and 'id' in m}
        # process each meal in history
        for hid in self.history_ids:
            meal = meal_map.get(hid)
            if not meal:
                continue
            tokens = []
            # split flavor and diet into individual tokens
            for part in (str(meal.get("flavor", "")).split(",") + str(meal.get("diet", "")).split(",")):
                for t in part.strip().split():
                    if t:
                        tokens.append(t.lower())
            # count tokens
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1
                total += 1
        # normalize counts to get weights 0..1
        if total > 0:
            self.token_weights = {k: v / total for k, v in token_counts.items()}

    def add_meal_to_history(self, meal_id):
        # simple validation
        if not isinstance(meal_id, str):
            raise TypeError("meal_id must be a string")
        self.history_ids.append(meal_id)

    def check_budget(self, price):
        # check if price fits within budget
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if self.budget is None:
            return True
        return price <= self.budget

    def __str__(self):
        # readable representation
        return f"UserPreferences(history_ids={self.history_ids}, budget={self.budget})"

    def __repr__(self):
        # developer-friendly representation
        return f"<UserPreferences {self}>"
