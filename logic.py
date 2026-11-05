import sqlite3
from datetime import datetime

conn = sqlite3.connect("tracker.db")
conn.execute("CREATE TABLE IF NOT EXISTS history (timestamp TEXT, category TEXT, xp INTEGER)")
conn.execute("CREATE TABLE IF NOT EXISTS categories (name TEXT PRIMARY KEY)")
conn.execute("CREATE TABLE IF NOT EXISTS rules (category TEXT, xp INTEGER, text TEXT)")
conn.commit()


def load_categories():
    result = {}
    for (name,) in conn.execute("SELECT name FROM categories"):
        result[name] = {}
    for category, xp, text in conn.execute("SELECT category, xp, text FROM rules ORDER BY xp"):
        result[category][str(xp)] = text
    return result
    

def add_xp(category, xp):
   conn.execute(
       "INSERT INTO history (timestamp, category, xp) VALUES (?, ?, ?)",
       (datetime.now().isoformat(), category, xp)
   )
   conn.commit()


def add_category(name, rules):
    try:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        return False
    conn.execute("INSERT INTO rules (category, xp, text) VALUES (?, ?, ?)", (name, 2, rules["2"]))
    conn.execute("INSERT INTO rules (category, xp, text) VALUES (?, ?, ?)", (name, 5, rules["5"]))
    conn.execute("INSERT INTO rules (category, xp, text) VALUES (?, ?, ?)", (name, 7, rules["7"]))
    conn.execute("INSERT INTO rules (category, xp, text) VALUES (?, ?, ?)", (name, 10, rules["10"]))
    conn.commit()
    return True
            

def calculate_stats():
    rows = conn.execute("SELECT category, SUM(xp) FROM history GROUP BY category").fetchall()
    categories_xp = {}
    for category, xp in rows:
        categories_xp[category] = xp
    total_xp = sum(categories_xp.values()) 
    level = total_xp // 100
    return total_xp, level, categories_xp


def delete_category(name):
    conn.execute("DELETE FROM rules WHERE category = ?", (name,))
    conn.execute("DELETE FROM categories WHERE name = ?", (name,))
    conn.commit()
    