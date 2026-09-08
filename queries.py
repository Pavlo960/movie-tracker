import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'films_config.settings')
django.setup()

from movies.models import Movie, Director, Genre
from django.db.models import Count


print('1. All movies:', Movie.objects.all())

print('2. Long movies (>150m):', Movie.objects.filter(duration__gt=150))

print('3. Nolan movies:', Movie.objects.filter(director__name='Christopher Nolan'))

print('4. Watched movies:', Movie.objects.filter(status='watched'))

print('5. Top-3 longest movies:', Movie.objects.order_by('-duration')[:3])

directors_count = Director.objects.annotate(movie_count=Count('movies'))
print('6. Movies per director:', [(d.name, d.movie_count) for d in directors_count])

sample_query = Movie.objects.filter(genre__name='Drama')
print('7. QuerySet:', sample_query)
print('7. Generated SQL:', sample_query.query)

