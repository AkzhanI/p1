from datetime import datetime 
import json
import os

def load_categories():
    if os.path.exists("categories.json"):
        with open("categories.json") as f:
            return json.load(f)
    else:
        return{}
    
def save_categories(data):
    with open("categories.json", "w") as f:
        json.dump(data, f)

def load_history():
    if os.path.exists("history.json"):
        with open("history.json") as f:
            return json.load(f)
    else:
        return []
def save_history(data):
    with open("history.json", "w") as f:
        json.dump(data, f)

def add_xp(category, xp):
    history = load_history()
    entry = {
        "timestamp": datetime.now().isoformat(), 
        "category": category, 
        "xp": xp
    }
    history.append(entry)
    save_history(history)

def calculate_stats():
    history = load_history()
    total_xp = 0
    categories_xp = {}
    for item in history:
        total_xp += item["xp"]
        if item["category"] in categories_xp:
            categories_xp[item["category"]] += item["xp"] 
        else:
                categories_xp[item["category"]] = item["xp"]
    level = total_xp // 100
    return total_xp, level, categories_xp

def show_stats():
    total_xp, level, categories_xp = calculate_stats()
    print(f"Level: {level}")
    print(f"XP: {total_xp}")
    for cat, xp in categories_xp.items():
        print(f"  {cat}: {xp} XP")
while True:
    print("\n1. Show statistics")
    print("2. add XP")
    print("3. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        show_stats()
    elif choice == "2":
        categories = load_categories()
        if not categories:
            print("no category")
        else:
            print("Categories:", list(categories.keys()))
            cat = input("enter the category name: ")
            xp = int(input("Enter XP amount: "))
            add_xp(cat, xp)
            print("Added!")
    elif choice == "3":
        break
    elif choice == "4":
        name = input("Category name: ")
        rule2 = input("Rule for +2 XP: ")
        rule5 = input("Rule for +5 XP: ")
        rule7 = input("Rule for +7 XP: ")
        rule10 = input("Rule for +10 XP: ")
        categories = load_categories()
        categories[name] = {
            "2": rule2,
            "5": rule5,
            "7": rule7,
            "10": rule10
        }
        save_categories(categories)
        print("Category added!")
    else:
        print("not yet implemented")