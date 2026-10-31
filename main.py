from datetime import datetime
import json
import os
import tkinter as tk

BG = "#1e1e2e"
FG = "white"
ACCENT = "#380b86"

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

def open_add_category():
    window = tk.Toplevel(root)
    window.title("new category")
    window.configure(bg=BG)
    window.geometry("300x400")
    tk.Label(window, text="category name", bg=BG, fg=FG, font=("Courier", 11)).pack(pady=5)
    name_entry = tk.Entry(window, font=("Courier", 11))
    name_entry.pack(pady=5)

    tk.Label(window, text="rules +2", bg=BG, fg=FG, font=("Courier", 11)).pack(pady=5)
    entry_plus2 = tk.Entry(window, font=("Courier", 11))
    entry_plus2.pack(pady=5)

    tk.Label(window, text="rules +5", bg=BG, fg=FG, font=("Courier", 11)).pack(pady=5)
    entry_plus5 = tk.Entry(window, font=("Courier", 11))
    entry_plus5.pack(pady=5)  

    tk.Label(window, text="rules +7", bg=BG, fg=FG, font=("Courier", 11)).pack(pady=5)
    entry_plus7 = tk.Entry(window, font=("Courier", 11))
    entry_plus7.pack(pady=5)  

    tk.Label(window, text="rules +10", bg=BG, fg=FG, font=("Courier", 11)).pack(pady=5)
    entry_plus10 = tk.Entry(window, font=("Courier", 11))
    entry_plus10.pack(pady=5)

    def save_category():
        name = name_entry.get()
        if name.strip() == "":
            return
        rules = {
            "2": entry_plus2.get(),
            "5": entry_plus5.get(),
            "7": entry_plus7.get(),
            "10": entry_plus10.get()
        }
        categories = load_categories()
        categories[name] = rules
        save_categories(categories)
        window.destroy()
        refresh()

    tk.Button(window, text="save", bg=ACCENT, fg=FG, font=("Courier", 11), width=20, command=lambda: save_category()).pack(pady=10
    
        
    )
def delete_category(name):
        categories = load_categories()
        del categories[name]
        save_categories(categories)
        
def  refresh():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    total_xp, level, categories_xp = calculate_stats()
    tk.Label(scrollable_frame, text=f"level: {level}", bg=BG, fg=FG, font=("Courier", 12), pady=4).pack()
    tk.Label(scrollable_frame, text=f"XP: {total_xp}", bg=BG, fg=FG, font=("Courier", 12), pady=4).pack()
    for cat, xp in categories_xp.items():
        tk.Label(scrollable_frame, text=f"{cat}: {xp} XP", bg=BG, fg=FG, font=("Courier", 11), pady=6, padx=10).pack()
    categories = load_categories()
    for cat, rules in categories.items():
        tk.Label(scrollable_frame, text=cat, bg=BG, fg=FG, font=("Courier", 11), pady=6, padx=10).pack()
        tk.Button(scrollable_frame, text="Delete", bg=ACCENT, fg=FG, font=("Courier", 11), width=28, command=lambda c=cat: [delete_category(c), refresh()]).pack(pady=10, padx=10)
        for xp_amount, rule in rules.items():
            tk.Button(scrollable_frame, text=f"{rule} +{xp_amount}", bg=ACCENT, fg=FG, font=("Courier", 11), width=28, pady=6, padx=10,  command=lambda c=cat, x=xp_amount: [add_xp(c, int(x)), refresh()]).pack()
    tk.Button(scrollable_frame, text="+ add category", bg=ACCENT, fg=FG, font=("Courier", 11), width=28, command=open_add_category).pack(pady=10)
    


root = tk.Tk()
root.title("Skill Tracker")
root.geometry("400x500")
root.configure(bg="#1e1e2e")
canvas = tk.Canvas(root, bg=BG, highlightthickness=0, bd=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=BG)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=(0, 0, 0, scrollable_frame.winfo_reqheight()))
)
frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
def center_frame(event):
    canvas.coords(frame_window, event.width // 2, 0)
canvas.bind("<Configure>", center_frame)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
refresh()
root.mainloop()
