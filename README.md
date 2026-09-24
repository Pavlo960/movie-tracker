# Movie Tracker

Movie Tracker is a feature-rich web application designed for film enthusiasts to manage their personal movie collections. It allows users to track watched films, organize a watchlist, customize the interface with dynamic themes and user profiles, and keep an interactive record of their viewing activity.

## Features
- User authentication (registration, login, logout, and profile management).
- Full CRUD operations for managing movies (add, view, edit, delete).
- Interactive filtering and sorting sidebar by genres, status, and search queries.
- Custom user avatars and theme color customization (background and accent colors).
- Watchlist and favorites management.

## Technologies
- Python, Django
- SQLite (Development) / PostgreSQL (Production ready)
- HTML5, CSS3, JavaScript
- Pillow (for image handling)
- django-environ (for environment configuration)

## How to Run Locally

```bash
git clone <your-fork-url>
cd films
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

## Live demo
Coming soon

## Screenshot
![Movie Tracker Screenshot](media\avatars\Screenshot_2025-03-18_201202.png)