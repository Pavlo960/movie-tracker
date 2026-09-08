from django.db import models
class Director(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Movie(models.Model):
    STATUS_CHOICES = [
        ('want', 'Хочу подивитись'),
        ('watching', 'Дивлюсь'),
        ('watched', 'Переглянуто'),
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

