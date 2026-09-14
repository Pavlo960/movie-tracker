from django.shortcuts import get_object_or_404, render
from .models import Director, Movie


def movie_list(request):
  movies = (
      Movie.objects.select_related('director').prefetch_related('genre').all()
  )
  return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, pk):
  movie = get_object_or_404(Movie, pk=pk)
  return render(request, 'movies/movie_detail.html', {'movie': movie})


def director_list(request):
  directors = Director.objects.prefetch_related('movies').all()
  return render(
      request, 'movies/director_list.html', {'directors': directors}
  )