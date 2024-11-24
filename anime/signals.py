from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

from .models import *

def animeshnik_profile(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='animeshnik')
        instance.groups.add(group)
        Animeshnik.objects.create(
            user = instance,
            user_name = instance.username,
            email = instance.email,
            )
        print("CREATED")
            
post_save.connect(animeshnik_profile, sender = User)

@receiver(pre_save, sender=Anime)
def log_anime_modification(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_anime = Anime.objects.get(pk=instance.pk)
            
            history = AnimeHistory.objects.create(
                anime=previous_anime,
                title=previous_anime.title,
                description=previous_anime.description,
                release_date=previous_anime.release_date,
                rating=previous_anime.rating,
                image=previous_anime.image,
                episodes=previous_anime.episodes,
                change_type='modified',
            )

            history.genres.set(previous_anime.genres.all())
        
        except Anime.DoesNotExist:
            pass

@receiver(pre_delete, sender=Anime)
def log_anime_deletion(sender, instance, **kwargs):
    if instance.pk:
        previous_anime = Anime.objects.get(pk=instance.pk)
        history = AnimeHistory.objects.create(
            anime=None,
            title=previous_anime.title,
            description=previous_anime.description,
            release_date=previous_anime.release_date,
            rating=previous_anime.rating,
            image=previous_anime.image,
            episodes=previous_anime.episodes,
            change_type='deleted',
        )
        
        history.genres.set(previous_anime.genres.all())