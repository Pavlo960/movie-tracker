from django.contrib import admin
from .models import Director, Genre, Movie

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'country')
    search_fields = ('name', 'country')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'status', 'director')
    list_filter = ('status', 'release_date', 'director', 'genre')
    search_fields = ('title', 'description')
    filter_horizontal = ('genre',)

    
