import os
import sqlite3
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "tracker.db")


def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS history (timestamp TEXT, category TEXT, xp INTEGER)")
    conn.execute("CREATE TABLE IF NOT EXISTS categories (name TEXT PRIMARY KEY, deleted INTEGER DEFAULT 0)")
    conn.execute("CREATE TABLE IF NOT EXISTS rules (category TEXT, xp INTEGER, text TEXT)")
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_rules_unique ON rules (category, xp)")
    conn.commit()
    conn.close()


init_db()


def load_categories(conn):
    result = {}
    for (name,) in conn.execute("SELECT name FROM categories WHERE deleted = 0"):
        result[name] = {}
    for category, xp, text in conn.execute("SELECT category, xp, text FROM rules ORDER BY xp"):
        if category in result:
            result[category][str(xp)] = text
    return result


def add_xp(conn, category, xp):
    if xp not in (2, 5, 7, 10):
        raise ValueError("xp должен быть 2, 5, 7 или 10")
    row = conn.execute(
        "SELECT 1 FROM categories WHERE name = ? AND deleted = 0", (category,)
    ).fetchone()
    if row is None:
        raise LookupError("категория не найдена")
    conn.execute(
        "INSERT INTO history (timestamp, category, xp) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), category, xp)
    )
    conn.commit()


def add_category(conn, name, rules):
    row = conn.execute("SELECT deleted FROM categories WHERE name = ?", (name,)).fetchone()
    if row is not None and row[0] == 0:
        return False
    with conn:
        if row is None:
            conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        else:
            conn.execute("UPDATE categories SET deleted = 0 WHERE name = ?", (name,))
            conn.execute("DELETE FROM rules WHERE category = ?", (name,))
        for xp in (2, 5, 7, 10):
            conn.execute(
                "INSERT INTO rules (category, xp, text) VALUES (?, ?, ?)",
                (name, xp, rules[str(xp)])
            )
    return True


def calculate_stats(conn):
    rows = conn.execute("SELECT category, SUM(xp) FROM history GROUP BY category").fetchall()
    categories_xp = {}
    for category, xp in rows:
        categories_xp[category] = xp
    total_xp = sum(categories_xp.values())
    level = total_xp // 100
    return total_xp, level, categories_xp


def delete_category(conn, name):
    conn.execute("UPDATE categories SET deleted = 1 WHERE name = ?", (name,))
    conn.commit()
    