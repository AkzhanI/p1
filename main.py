from datetime import datetime
import json
import os
import tkinter as tk

BG = "#1e1e2e"
FG = "white"
ACCENT = "#7c3aed"

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

def  refresh():
    for widjet in root.winfo_children():
        widjet.destroy()
    total_xp, level, categoties_xp = calculate_stats()
    tk.Label(root, text=f"level: {level}", bg=BG, fg=FG, font=("Courier", 12), pady=4).pack()
    tk.Label(root, text=f"XP: {total_xp}", bg=BG, fg=FG, font=("Courier", 12), pady=4).pack()
    for cat, xp in categoties_xp.items():
        tk.Label(root, text=f"{cat}: {xp} XP", bg=BG, fg=FG, font=("Courier", 11), pady=6, padx=10).pack()
    categories = load_categories()
    for cat, rules in categories.items():
        tk.Label(root, text=cat, bg=BG, fg=FG, font=("Courier", 11), pady=6, padx=10).pack()
        for xp_amount, rule in rules.items():
            tk.Button(root, text=f"{rule} +{xp_amount}", bg=ACCENT, fg=FG, font=("Courier", 11), pady=6, padx=10, width=20, command=lambda c=cat, x=xp_amount: [add_xp(c, int(x)), refresh()]).pack()

root = tk.Tk()
root.title("Skill Tracker")
root.geometry("400x500")
root.configure(bg="#1e1e2e")
refresh()
root.mainloop()