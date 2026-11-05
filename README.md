# Skill Tracker
[![Lint](https://github.com/AkzhanI/p1/actions/workflows/lint.yml/badge.svg)](https://github.com/AkzhanI/p1/actions/workflows/lint.yml)

A small XP tracker for my skills. I make a category (sport, english, whatever), write four rules for it worth +2, +5, +7 and +10 XP, and press a rule every time I do it. 100 XP = 1 level.

It's my learning project. First it was a script with JSON files, then I moved everything to SQLite. Next I want to make a web version on FastAPI.

## What it does

- categories with 4 custom rules each
- total XP, level (total_xp // 100) and XP per category
- two interfaces: a terminal menu and a Tkinter window. Both use the same logic

## Files

- logic.py: all the logic and database work. CLI and GUI only call functions from here
- tracker.py: terminal version
- main.py: Tkinter version
- tracker.db: created on first run, not in git

## Database

SQLite, three tables:

- categories(name): name is the primary key, so no duplicates
- rules(category, xp, text): the four rules of each category
- history(timestamp, category, xp): every XP entry

Stats are counted by the database itself:

SELECT category, SUM(xp) FROM history GROUP BY category;
If I delete a category, its rules are gone, but its XP stays in history. So I don't lose XP by accident.

## Run

python3 tracker.py
python3 main.py
Only Python 3 is needed, sqlite3 is built in. The GUI needs a screen, so run it on the host machine, not in the dev container. The CLI works anywhere.

There is a dev container config for VS Code: open the folder and choose "Reopen in Container".

Ruff checks the code on every push (GitHub Actions).

## TODO

- [x] history: JSON -> SQLite
- [x] categories and rules: JSON -> SQLite
- [ ] show "category already exists" message in CLI and GUI
- [ ] web version on FastAPI (one connection per request, because a SQLite connection can't be shared between threads)