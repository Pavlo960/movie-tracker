# Movie Tracker

Django application for tracking movies, directors, and genres with watch status management.

## Features
- List, view, registration, and CRUD operations for movies, directors, and genres
- Watch status management for films

## Models
- **Director** — director (name, country, birth date)
- **Genre** — genre
- **Movie** — movie (ForeignKey to Director, ManyToMany to Genre, status via choices)

## Technologies
Python, Django, SQLite (development) / PostgreSQL (production, if available)

## How to run locally

```bash
python -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env        
python manage.py migrate
python manage.py runserver
```

## Admin screenshot
![admin](screenshots/photo_2026-09-24_17-58-11.jpg)

## Live demo
Cooming soon...
