# Movie Tracker

Django application for tracking movies, directors, and genres with watch status management.

## Models
- Director — director (name, country, birth date)
- Genre — genre
- Movie — movie (ForeignKey to Director, ManyToMany to Genre, status via choices)

## How to run
python -m venv venv
.\venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver

## Admin screenshot
![admin](screenshots/screenshot.png)