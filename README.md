# Skill Tracker

A tool for tracking skills and learning progress through a gamified XP system. Available in two versions: a desktop app (Tkinter) and a CLI version (Docker-ready).

## Features

- Custom categories with configurable XP rules (+2 / +5 / +7 / +10)
- XP and level tracking based on activity history
- Category deletion (history is preserved)
- Scrollable category list (Canvas + Scrollbar) in the desktop version
- Data persistence via JSON (categories.json, history.json)

## Technologies

- Python
- Tkinter
- JSON
- Docker

## Running

### Desktop version (Tkinter)

```bash
python3 main.py
```
### CLI version (Docker)

No Python installation needed, only Docker. Data is stored in a Docker volume, so it persists between runs.

```bash
docker build -t skill-tracker .
docker run -it -v tracker-data:/data skill-tracker
```
## Status

Work in progress.
