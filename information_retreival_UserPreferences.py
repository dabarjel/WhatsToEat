# --- Simple UserPreferences class ---
class UserPreferences:
    """
    This class represents the user's meal preferences.
    """

    def __init__(self, history_ids=None, budget=None):
        self.history_ids = list(history_ids) if history_ids else []
        self.budget = budget
        self.token_weights = {}

    def update_preferences(self, meals):
        """
        Learn simple preference weights from history meals.
        """
        token_counts = {}
        total = 0
        meal_map = {m['id']: m for m in meals if 'id' in m}
        for hid in self.history_ids:
            meal = meal_map.get(hid)
            if not meal:
                continue
            # combine flavor and diet tokens
            tokens = []
            for part in (str(meal.get("flavor", "")).split(",") + str(meal.get("diet", "")).split(",")):
                for t in part.strip().split():
                    if t:
                        tokens.append(t.lower())
            for t in tokens:
                token_counts[t] = token_counts.get(t, 0) + 1
                total += 1
        if total > 0:
            self.token_weights = {k: v / total for k, v in token_counts.items()}

    def add_meal_to_history(self, meal_id):
        self.history_ids.append(meal_id)

    def check_budget(self, price):
        if self.budget is None:
            return True
        return price <= self.budget

    def __str__(self):
        return f"UserPreferences(history_ids={self.history_ids}, budget={self.budget})"

    def __repr__(self):
        return f"<UserPreferences {self}>"
