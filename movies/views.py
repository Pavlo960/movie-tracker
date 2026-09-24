from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from .forms import ReviewForm
from .models import Director, Genre, Movie, UserProfile


class SignUpView(CreateView):
  form_class = UserCreationForm
  template_name = 'registration/signup.html'
  success_url = reverse_lazy('login')


class MyMoviesView(LoginRequiredMixin, ListView):
  model = Movie
  template_name = 'movies/movie_list.html'
  context_object_name = 'movies'
  paginate_by = 6

  def get_queryset(self):
    queryset = super().get_queryset()

    search_query = self.request.GET.get('search')
    if search_query:
      queryset = queryset.filter(title__icontains=search_query)

    genre_slug = self.request.GET.get('genre')
    if genre_slug:
      queryset = queryset.filter(genre__name__iexact=genre_slug)

    status_filter = self.request.GET.get('status')
    if status_filter:
      queryset = queryset.filter(status=status_filter)

    sort_by = self.request.GET.get('sort')
    if sort_by == 'title':
      queryset = queryset.order_by('title')
    elif sort_by == '-title':
      queryset = queryset.order_by('-title')
    elif sort_by == 'release_date':
      queryset = queryset.order_by('-release_date')
    elif sort_by == 'duration':
      queryset = queryset.order_by('-duration')

    return queryset.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['genres'] = Genre.objects.all()
    context['statuses'] = Movie._meta.get_field('status').choices
    return context


class MovieListView(ListView):
  model = Movie
  template_name = 'movies/movie_list.html'
  context_object_name = 'movies'
  paginate_by = 6

  def get_queryset(self):
    queryset = super().get_queryset()

    search_query = self.request.GET.get('search')
    if search_query:
      queryset = queryset.filter(title__icontains=search_query)

    genre_slug = self.request.GET.get('genre')
    if genre_slug:
      queryset = queryset.filter(genre__name__iexact=genre_slug)

    status_filter = self.request.GET.get('status')
    if status_filter:
      queryset = queryset.filter(status=status_filter)

    sort_by = self.request.GET.get('sort')
    if sort_by == 'title':
      queryset = queryset.order_by('title')
    elif sort_by == '-title':
      queryset = queryset.order_by('-title')
    elif sort_by == 'release_date':
      queryset = queryset.order_by('-release_date')
    elif sort_by == 'duration':
      queryset = queryset.order_by('-duration')
    else:
      queryset = queryset.order_by('-release_date')

    return queryset.distinct()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['genres'] = Genre.objects.all()
    context['statuses'] = Movie._meta.get_field('status').choices
    return context


class MovieDetailView(DetailView):
  model = Movie
  template_name = 'movies/movie_detail.html'
  context_object_name = 'movie'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['review_form'] = ReviewForm()
    reviews = self.object.reviews.all()
    if reviews.exists():
      context['average_rating'] = sum(r.rating for r in reviews) / reviews.count()
    else:
      context['average_rating'] = None
    return context

  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('login')

    self.object = self.get_object()
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.movie = self.object
      review.user = request.user
      review.save()
      return redirect('movie_detail', pk=self.object.pk)

    context = self.get_context_data()
    context['review_form'] = form
    return self.render_to_response(context)


class MovieCreateView(LoginRequiredMixin, CreateView):
  model = Movie
  fields = [
      'title',
      'description',
      'duration',
      'release_date',
      'status',
      'director',
      'genre',
  ]
  template_name = 'movies/movie_form.html'

  def form_valid(self, form):
    form.instance.owner = self.request.user
    return super().form_valid(form)


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Movie
  fields = [
      'title',
      'description',
      'duration',
      'release_date',
      'status',
      'director',
      'genre',
  ]
  template_name = 'movies/movie_form.html'

  def test_func(self):
    return self.get_object().owner == self.request.user


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Movie
  template_name = 'movies/movie_confirm_delete.html'
  success_url = reverse_lazy('movie_list')

  def test_func(self):
    return self.get_object().owner == self.request.user


class DirectorListView(ListView):
  model = Director
  paginate_by = 5
  ordering = ['name']
  context_object_name = 'directors'
  template_name = 'movies/director_list.html'

  def get_queryset(self):
    queryset = super().get_queryset()
    name = self.request.GET.get('name')
    if name:
      queryset = queryset.filter(name__icontains=name)
    return queryset


class DirectorDetailView(DetailView):
  model = Director
  context_object_name = 'director'
  template_name = 'movies/director_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['movies'] = self.object.movies.all()
    return context


class DirectorCreateView(CreateView):
  model = Director
  fields = ['name', 'birth_date', 'country']
  template_name = 'movies/director_form.html'


class DirectorUpdateView(UpdateView):
  model = Director
  fields = ['name', 'birth_date', 'country']
  template_name = 'movies/director_form.html'


class DirectorDeleteView(DeleteView):
  model = Director
  template_name = 'movies/director_confirm_delete.html'
  success_url = reverse_lazy('director_list')


class GenreListView(ListView):
  model = Genre
  paginate_by = 5
  ordering = ['name']
  context_object_name = 'genres'
  template_name = 'movies/genre_list.html'

  def get_queryset(self):
    queryset = super().get_queryset()
    name = self.request.GET.get('name')
    if name:
      queryset = queryset.filter(name__icontains=name)
    return queryset


class GenreDetailView(DetailView):
  model = Genre
  context_object_name = 'genre'
  template_name = 'movies/genre_detail.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['movies'] = self.object.movies.all()
    return context


class GenreCreateView(CreateView):
  model = Genre
  fields = ['name']
  template_name = 'movies/genre_form.html'


class GenreUpdateView(UpdateView):
  model = Genre
  fields = ['name']
  template_name = 'movies/genre_form.html'


class GenreDeleteView(DeleteView):
  model = Genre
  template_name = 'movies/genre_confirm_delete.html'
  success_url = reverse_lazy('genre_list')


class UserProfileView(LoginRequiredMixin, TemplateView):
  template_name = 'movies/profile.html'

  def post(self, request, *args, **kwargs):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    accent_color = request.POST.get('accent_color')
    bg_color = request.POST.get('bg_color')

    if accent_color:
      user_profile.accent_color = accent_color
    if bg_color:
      user_profile.bg_color = bg_color

    avatar = request.FILES.get('avatar')
    if avatar:
      user_profile.avatar = avatar

    user_profile.save()
    return redirect('profile')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    user = self.request.user
    
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    self.request.session['user_accent'] = user_profile.accent_color
    self.request.session['user_bg'] = user_profile.bg_color
    watchlist_movies = user.watchlist_movies.all()
    user_movies = user.movies.all()

    total_minutes = 0
    for m in user_movies:
      try:
        total_minutes += int(m.duration)
      except (ValueError, TypeError):
        pass

    total_hours = round(total_minutes / 60, 1)

    context['user_profile'] = user_profile  
    context['watchlist_movies'] = watchlist_movies
    context['user_movies'] = user_movies
    context['total_hours'] = total_hours
    context['total_movies_count'] = user_movies.count()
    return context


def change_theme(request):
  accent_color = request.GET.get('accent')
  bg_color = request.GET.get('bg')

  if accent_color:
    request.session['user_accent'] = accent_color
  if bg_color:
    request.session['user_bg'] = bg_color
  request.session.modified = True

  if request.user.is_authenticated:
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if accent_color:
      user_profile.accent_color = accent_color
    if bg_color:
      user_profile.bg_color = bg_color
    user_profile.save()

  return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'profile'))

def toggle_watchlist(request, pk):
  if not request.user.is_authenticated:
    return redirect('login')
  movie = get_object_or_404(Movie, pk=pk)
  if movie.watchlist.filter(pk=request.user.pk).exists():
    movie.watchlist.remove(request.user)
  else:
    movie.watchlist.add(request.user)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'movie_list'))


