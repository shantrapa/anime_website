from django.db import models
from django.contrib.auth.models import User

class Animeshnik(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length = 50, unique = True, default="Unknown User")
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    gender = models.CharField(max_length = 15, null = True, blank = True, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather not say', 'Rather not say'),
    ])
    email = models.EmailField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(default = "profile.png", null=True, blank=True)

    def __str__(self):
        return self.user_name
    
class Moderator(models.Model):
    user = models.OneToOneField(User, null=True, blank = True, on_delete=models.CASCADE)
    user_name = models.CharField(max_length = 50, unique = True, default="Unknown User")
    first_name = models.CharField(max_length = 50, null = True, blank = True)
    last_name = models.CharField(max_length = 50, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    gender = models.CharField(max_length = 15, null = True, blank = True, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather not say', 'Rather not say'),
    ])
    email = models.CharField(max_length = 50, null = True, blank = True)
    profile_pic = models.ImageField(default = "profile.png", null=True, blank=True)

    def __str__(self):
        return self.user_name

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    image = models.URLField(default='default_anime.png', null = True, blank = True)
    episodes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class AnimeHistory(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    image = models.URLField(default='default_anime.png', null=True, blank=True)
    episodes = models.IntegerField(null=True, blank=True)
    change_type = models.CharField(max_length=20, choices=[
        ('deleted', 'Deleted'),
        ('modified', 'Modified'),
    ])
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.change_type == 'deleted':
            return f"{self.title} - {self.change_type} at {self.changed_at}"
        else:
            return f"{self.anime.title} - {self.change_type} at {self.changed_at}"
    
class UserAnimeStatus(models.Model):
    STATUS_CHOICES = [
        ('Буду смотреть', 'Буду смотреть'),
        ('Смотрю', 'Смотрю'),
        ('Просмотрено', 'Просмотрено'),
    ]
    
    user = models.ForeignKey(Animeshnik, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user} - {self.anime} ({self.status})"