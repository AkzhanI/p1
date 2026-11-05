from logic import (
    add_category,
    add_xp,
    calculate_stats,
    delete_category,
    load_categories,
)


def show_stats():
    total_xp, level, categories_xp = calculate_stats()
    print(f"Level: {level}")
    print(f"XP: {total_xp}")
    for cat, xp in categories_xp.items():
        print(f"  {cat}: {xp} XP")
while True:
    print("\n1. Show statistics")
    print("2. add XP")
    print("3. add category")
    print("4. delete category")
    print("5. Exit")
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
        name = input("Category name: ")
        rule2 = input("Rule for +2 XP: ")
        rule5 = input("Rule for +5 XP: ")
        rule7 = input("Rule for +7 XP: ")
        rule10 = input("Rule for +10 XP: ")
        rules = {"2": rule2,  "5": rule5, "7": rule7, "10": rule10}
        add_category(name, rules)
        print("Category added!")
    elif choice == "4":
        categories = load_categories()
        if not categories:
            print("no category")
        else:
            print("Categories:", list(categories.keys()))
            name = input("enter the category name to delete: ")
            if name in categories:
                delete_category(name)
                print("Deleted!")
            else:
                print("no such category")
    elif choice == "5":
        break
        
    else:
        print("not yet implemented")