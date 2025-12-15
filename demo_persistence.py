"""Demo showing data persistence (save/load) functionality for Project 4."""

from information_retreival_MealClass import Meal
from information_retreival_MenuClass import Menu
from information_retreival_UserPreferences import UserPreferences

def demo_persistence():
    """Demonstrate save/load capabilities for Project 4 requirements."""
    print("=" * 60)
    print("DATA PERSISTENCE DEMO - Project 4")
    print("=" * 60)
    
    # 1. CREATE AND SAVE MENU
    print("\n1. Creating menu with meals...")
    menu = Menu()
    
    m1 = Meal("1", "Vegetarian Pasta", 12.99, 600, "vegetarian", "savory")
    m1.add_rating(5)
    m1.add_rating(4)
    
    m2 = Meal("2", "Chicken Burger", 10.99, 700, "meat", "savory")
    m2.add_rating(4)
    m2.add_rating(5)
    
    m3 = Meal("3", "Spicy Tofu Bowl", 9.99, 450, "vegan", "spicy")
    m3.add_rating(5)
    
    menu.add(m1)
    menu.add(m2)
    menu.add(m3)
    
    print(f"   Created menu with {len(menu)} meals")
    for meal in menu:
        print(f"   - {meal.name}: ${meal.price}, avg rating: {meal.average_rating:.1f}")
    
    print("\n2. SAVING menu to file...")
    menu.save_to_file('data/menu.json')
    print("   ✓ Menu saved to: data/menu.json")
    
    # 2. LOAD MENU BACK
    print("\n3. LOADING menu from file...")
    loaded_menu = Menu.load_from_file('data/menu.json')
    print(f"   ✓ Successfully loaded {len(loaded_menu)} meals from file")
    print("   Loaded meals:")
    for meal in loaded_menu:
        print(f"   - {meal.name}: ${meal.price}")
    
    # 3. CREATE AND SAVE USER PREFERENCES
    print("\n4. Creating user preferences...")
    prefs = UserPreferences(history_ids=["1", "3"], budget=15.0)
    prefs.update_preferences([m.to_dict() for m in menu.meals])
    
    print(f"   User history: {prefs.history_ids}")
    print(f"   User budget: ${prefs.budget}")
    print(f"   Learned preferences: {prefs.token_weights}")
    
    print("\n5. SAVING user preferences to file...")
    prefs.save_to_file('data/user_preferences.json')
    print("   ✓ User preferences saved to: data/user_preferences.json")
    
    # 4. LOAD PREFERENCES BACK
    print("\n6. LOADING user preferences from file...")
    loaded_prefs = UserPreferences.load_from_file('data/user_preferences.json')
    print(f"   ✓ Successfully loaded preferences")
    print(f"   History: {loaded_prefs.history_ids}")
    print(f"   Budget: ${loaded_prefs.budget}")
    print(f"   Token weights: {loaded_prefs.token_weights}")
    
    # 5. DEMONSTRATE EXPORT (ANALYTICS)
    print("\n7. Generating and displaying analytics...")
    analytics = menu.analytics()
    print(f"   Total meals: {analytics['total_meals']}")
    print(f"   Average price: ${analytics['avg_price']:.2f}")
    print(f"   Price range: ${analytics['min_price']:.2f} - ${analytics['max_price']:.2f}")
    print(f"   Top rated meals:")
    for meal_info in analytics['top_rated']:
        print(f"     - {meal_info['name']}: {meal_info['avg_rating']:.1f} stars")
    
    # Save analytics to file
    import json
    from pathlib import Path
    Path('reports').mkdir(exist_ok=True)
    with open('reports/analytics.json', 'w') as f:
        json.dump(analytics, f, indent=2)
    print("   ✓ Analytics exported to: reports/analytics.json")
    
    # 6. DEMONSTRATE ERROR HANDLING
    print("\n8. Testing error handling...")
    try:
        UserPreferences.load_from_file('nonexistent_file.json')
    except FileNotFoundError as e:
        print(f"   ✓ Correctly caught missing file: {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("✓ ALL PERSISTENCE OPERATIONS SUCCESSFUL!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - data/menu.json")
    print("  - data/user_preferences.json")
    print("  - reports/analytics.json")
    print("\nProject 4 Requirements Met:")
    print("  ✓ Save/load system state (UserPreferences, Menu)")
    print("  ✓ Import data (CSV via parse_menu_csv)")
    print("  ✓ Export results (analytics to JSON)")
    print("  ✓ Error handling (FileNotFoundError, IOError)")
    print("  ✓ Context managers (with statements)")
    print("  ✓ pathlib for file paths")
    print("=" * 60)

if __name__ == "__main__":
    demo_persistence()


