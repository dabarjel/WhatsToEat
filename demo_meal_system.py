"""Demo of meal recommendation system."""

from meal_items import StandardMeal, SpecialtyMeal, BundleMeal
from menu_class_compositon import Menu
from recommendation_class import Recommendations


def demo_inheritance():
    """Show inheritance hierarchy."""
    print("=== Inheritance Demo ===")
    print("Creating different meal types (all inherit from AbstractMealItem)")

    standard = StandardMeal("1", "Pasta Carbonara", 12.99, 650, "vegetarian", "creamy")
    specialty = SpecialtyMeal("2", "Truffle Risotto", 28.99, 580, "vegetarian", "savory", 45)
    bundle = BundleMeal("3", "Family Combo", 35.99, 2100, "mixed", "varied", 4, 25.0)

    print(f"Standard: {standard.name} - ${standard.price}")
    print(f"Specialty: {specialty.name} - ${specialty.price}")
    print(f"Bundle: {bundle.name} - ${bundle.price}")
    print()


def demo_polymorphism():
    """Show polymorphic behavior."""
    print("=== Polymorphism Demo ===")
    print("Same method calls, different behaviors:")

    meals = [
        StandardMeal("1", "Basic Meal", 10.0, 500, "vegetarian", "mild"),
        SpecialtyMeal("2", "Premium Meal", 10.0, 500, "vegetarian", "mild", 40),
        BundleMeal("3", "Combo Meal", 10.0, 500, "mixed", "varied", 3, 20.0)
    ]

    for meal in meals:
        meal.add_rating(4)

    print("\nValue scores (different calculation per type):")
    for meal in meals:
        score = meal.calculate_value_score()
        print(f"  {meal.__class__.__name__}: {score:.2f}")

    print("\nPreparation info (different message per type):")
    for meal in meals:
        print(f"  {meal.get_preparation_info()}")
    print()


def demo_composition():
    """Show composition relationships."""
    print("=== Composition Demo ===")
    print("Menu has-a collection of meals")
    print("Recommendations has-a menu")

    menu = Menu()

    menu.add_meal(StandardMeal("1", "Garden Salad", 7.99, 250, "vegetarian", "fresh"))
    menu.add_meal(SpecialtyMeal("2", "Filet Mignon", 34.99, 650, "meat", "rich", 40))
    menu.add_meal(BundleMeal("3", "Date Night", 49.99, 1400, "mixed", "romantic", 4, 30.0))

    print(f"\nMenu contains {len(menu)} meals")

    rec = Recommendations(menu)
    rec.add_to_history("1")
    rec.add_to_history("2")

    print(f"Recommendation history: {len(rec.get_history())} selections")

    suggestions = rec.recommend_by_value(top_k=2)
    print(f"\nTop 2 recommendations by value:")
    for meal in suggestions:
        print(f"  {meal.name} - Score: {meal.calculate_value_score():.2f}")
    print()


def demo_complete_system():
    """Show everything working together."""
    print("=== Complete System Demo ===")

    menu = Menu()

    m1 = StandardMeal("1", "Caesar Salad", 9.99, 350, "vegetarian", "tangy")
    m1.add_rating(4)
    m1.add_rating(5)

    m2 = SpecialtyMeal("2", "Lobster Tail", 39.99, 450, "seafood", "buttery", 35)
    m2.add_rating(5)
    m2.add_rating(5)

    m3 = BundleMeal("3", "Lunch Special", 12.99, 900, "mixed", "varied", 3, 20.0)
    m3.add_rating(4)

    menu.add_meal(m1)
    menu.add_meal(m2)
    menu.add_meal(m3)

    print(f"Menu has {len(menu)} meals")

    print("\nFiltered by diet:")
    veg_meals = menu.filter_by_diet("vegetarian")
    print(f"  Vegetarian options: {len(veg_meals)}")

    print("\nFiltered by price:")
    affordable = menu.filter_by_price(15.0)
    print(f"  Under $15: {len(affordable)}")

    rec = Recommendations(menu)

    print("\nTop recommendations:")
    top_meals = rec.recommend_by_value(top_k=3)
    for i, meal in enumerate(top_meals, 1):
        print(f"  {i}. {meal.name} ({meal.__class__.__name__})")
        print(f"     ${meal.price} - {meal.get_preparation_info()}")
    print()


if __name__ == "__main__":
    demo_inheritance()
    demo_polymorphism()
    demo_composition()
    demo_complete_system()
    print("=== Demo Complete ===")
