from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),
    
    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/my/', views.MyMoviesView.as_view(), name='my_movies'),
    path('movies/new/', views.MovieCreateView.as_view(), name='movie_create'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie_update'),
    path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),

    path('directors/', views.DirectorListView.as_view(), name='director_list'),
    path('directors/new/', views.DirectorCreateView.as_view(), name = 'director_create'),
    path('directors/<int:pk>/', views.DirectorDetailView.as_view(), name='director_detail'),
    path('directors/<int:pk>/edit/', views.DirectorUpdateView.as_view(), name='director_update'),
    path('directors/<int:pk>/delete/', views.DirectorDeleteView.as_view(), name='director_delete'),

    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/new/', views.GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genres/<int:pk>/edit/', views.GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),

    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path(
        'movie/<int:pk>/watchlist/',
        views.toggle_watchlist,
        name='toggle_watchlist',
    ),
    path('profile/theme/', views.change_theme, name='change_theme'),
    ]