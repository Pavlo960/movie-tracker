from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Director(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('director_detail', kwargs={'pk': self.pk})
    
class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'pk': self.pk})
    
class Movie(models.Model):
    STATUS_CHOICES = [
        ('want', 'want to watch'),
        ('watching', 'watching'),
        ('watched', 'watched'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Тривалість у хвилинах")
    release_date = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        )
    
    director = models.ForeignKey(Director, 
        on_delete=models.CASCADE,
        related_name='movies',
        )
    
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='movies'
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='movies', 
        null=True,
        )
    watchlist = models.ManyToManyField(
        User,
        related_name='watchlist_movies',
        blank=True

    )
    poster_url = models.URLField(max_length=500, blank=True, null=True)

class Review(models.Model):
  movie = models.ForeignKey(
      'Movie', on_delete=models.CASCADE, related_name='reviews'
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  rating = models.PositiveIntegerField(
      validators=[MinValueValidator(1), MaxValueValidator(10)]
  )
  comment = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

#   class Meta:
#     unique_together = ('movie', 'user')  
#     ordering = ['-created_at']

  def __str__(self):
    return f'{self.user.username} - {self.movie.title} ({self.rating}/10)'

class UserProfile(models.Model):
  user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name='profile'
  )
  avatar = models.ImageField(
      upload_to='avatars/', blank=True, null=True
  )
  accent_color = models.CharField(
      max_length=20, default='#38bdf8'
  ) 
  bg_color = models.CharField(max_length=20, default='#0f172a')
    
  def __str__(self):
    return f'Profile of {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()
