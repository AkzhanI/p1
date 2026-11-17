# Skill Tracker

[![Lint](https://github.com/AkzhanI/p1/actions/workflows/lint.yml/badge.svg)](https://github.com/AkzhanI/p1/actions/workflows/lint.yml)

A small XP tracker for my skills. I make a category (sport, english, whatever), write four rules for it worth +2, +5, +7 and +10 XP, and press a rule every time I do it. 100 XP = 1 level.

It's my learning project. First it was a script with JSON files, then I moved everything to SQLite, and now it also has a web API on FastAPI that runs in Docker.

## What it does

- categories with 4 custom rules each
- total XP, level (total_xp // 100) and XP per category
- three interfaces: a terminal menu, a Tkinter window and a REST API. All of them use the same logic

## Files

- logic.py: all the logic and database work. CLI, GUI and API only call functions from here
- tracker.py: terminal version
- main.py: Tkinter version
- api.py: FastAPI version
- requirements.txt: dependencies for the API (fastapi, uvicorn)
- Dockerfile: image for the API
- ruff.toml: linter settings
- tracker.db: created on first run, not in git

## Database

SQLite, three tables:

- categories(name, deleted): name is the primary key, so no duplicates. deleted = 1 means the category is hidden
- rules(category, xp, text): the four rules of each category, unique per (category, xp)
- history(timestamp, category, xp): every XP entry

Stats are counted by the database itself:

SELECT category, SUM(xp) FROM history GROUP BY category;
If I delete a category, it is only hidden (deleted flag). Its rules and XP history stay, so I never lose XP by accident. If I create a category with the same name again, it comes back with the new rules and the old XP.

Every function in logic.py takes a connection as the first argument. The API opens one connection per request, because a SQLite connection can't be shared between threads.

## Run

CLI and GUI need only Python 3 (sqlite3 is built in):

python3 tracker.py
python3 main.py
The GUI needs a screen, so run it on the host machine, not in the dev container. The CLI works anywhere.

API:

pip install -r requirements.txt
uvicorn api:app --reload
Docs page with a "try it out" button: http://127.0.0.1:8000/docs

API in Docker:

docker build -t tracker-api .
docker run -p 8000:8000 -v tracker-data:/data tracker-api
The database lives in the tracker-data volume, so it survives container restarts. If port 8000 is busy, use -p 8001:8000.

## API endpoints

- GET /categories: active categories with their rules
- POST /categories: create a category (name and rules with keys 2, 5, 7, 10)
- DELETE /categories/{name}: hide a category
- POST /xp: add XP (category and xp, one of 2, 5, 7, 10)
- GET /stats: total XP, level and XP per category

Errors: 404 if the category is not found, 409 if it already exists, 422 for wrong data.

## Dev

There is a dev container config for VS Code: open the folder and choose "Reopen in Container".

Ruff checks the code on every push (GitHub Actions).

## TODO

- [x] history: JSON -> SQLite
- [x] categories and rules: JSON -> SQLite
- [x] show "category already exists" message in CLI and GUI
- [x] web API on FastAPI (one connection per request)
- [x] Dockerfile for the API
- [ ] build the Docker image in GitHub Actions
- [ ] simple web page that talks to the API