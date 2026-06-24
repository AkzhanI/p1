from datetime import datetime
import json
import os

def load_categories():
    if os.path.exists("categories.json"):
        with open("categories.json") as f:
            return json.load(f)
    else:
        return {}
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

def colculate_stats():
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
print(colculate_stats())