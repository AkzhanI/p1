import json
import os
import sqlite3
from datetime import datetime

conn = sqlite3.connect("tracker.db")
conn.execute("CREATE TABLE IF NOT EXISTS history (timestamp TEXT, category TEXT, xp INTEGER)")
conn.commit()


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
   conn.execute(
       "INSERT INTO history (timestamp, category, xp) VALUES (?, ?, ?)",
       (datetime.now().isoformat(), category, xp)
   )
   conn.commit()

def calculate_stats():
    rows = conn.execute("SELECT category, SUM(xp) FROM history GROUP BY category").fetchall()
    categories_xp = {}
    for category, xp in rows:
        categories_xp[category] = xp
    total_xp = sum(categories_xp.values()) 
    level = total_xp // 100
    return total_xp, level, categories_xp

def delete_category(name):
        categories = load_categories()
        del categories[name]
        save_categories(categories)